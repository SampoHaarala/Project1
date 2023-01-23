from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import sqlite3
import requests

# Create your views here.

def login(request):
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = str(request.POST.get('password'))
        con = sqlite3.connect('users.sqlite3')
        cur = con.cursor()
        #FLAW1 FIX: Check for harming input like: "DROP TABLE Users"
        response = cur.execute("SELECT name FROM Users WHERE password='%s'" % (passw)).fetchone() #FLAW 1: This line has an injection vulnerability. 
        #FLAW1 FIX: Above line needs to be changed to:
        #response = cur.execute("SELECT password FROM Users WHERE name=’%s’" % (usern)).fetchone()
        if response == None:
            return redirect('/')
        print(response)
        if response == usern: #FLAW1 FIX: Needs to be changed to: if response == passw:
            return redirect('account/' + usern)
        else:
            return redirect('/')
    return render(request, 'login.html')

#FLAW4 FIX:
test_transfer = {}

def set_test_transfer(user, to, amount):
    global test_transfer
    test_transfer[user] = [to, str(amount)]

def test_test_transfer(user, to, amount):
    if to == test_transfer[user][0] and str(amount) == test_transfer[user][1]:
        return true
    else:
        return false
    
def test_transfer(request, user):
    if request.method == 'POST':
        to = request.POST.get('to')
        amount = request.POST.get('amount')
        set_test_transfer(user, to, amount)
        return render(request, 'test_transfer.html', {'to': to, 'amount': amount}) 
    #Here 'test_transfer.html' should be a template that just shows that transfer request data wasn't tampered with.
    #After the request is confirmed the actual transfer request is sent.

#FLAW4: No protection against request tampering when transfering money.
def transfer(request, user):
    if request.method == 'POST':
        to = request.POST.get('to')
        amount = request.POST.get('amount')
        #FLAW4 FIX: Check that the test_transfer matches.
        #if test_test_transfer(to, amount):
        if amount != None and to != None:
            amount = int(amount)
            con = sqlite3.connect('users.sqlite3')
            cur = con.cursor()
            balanceS = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (user)).fetchone()[0]
            print(balanceS)
            balanceT = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (to)).fetchone()[0]
            print(balanceT)

            #FLAW3: Transfering minus amounts causes the sender to receive
            #FLAW3 FIX: Set up a if-statement that checks that the amount is valid.
            #if amount <= balanceS and 0 < amount:
            balanceS -= amount
            balanceT += amount
            #else:
            #   return redirect('/account/' + user) #Possibly implement an error message for the user.

            print(cur.execute("UPDATE Users SET balance='%s' WHERE name='%s'" % (balanceS, user)).fetchone())
            print(cur.execute("UPDATE Users SET balance='%s' WHERE name='%s'" % (balanceT, to)).fetchone())
        
            balanceS = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (user)).fetchone()[0]
            print(balanceS)
            balanceT = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (to)).fetchone()[0]
            print(balanceT)

            con.commit()
            cur.close()

    return redirect('/account/' + user)


def account(request, user):
    if request.method == 'GET':
        con = sqlite3.connect('users.sqlite3')
        cur = con.cursor()
        balance = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (user)).fetchone()[0]
        usersRaw = cur.execute("SELECT name FROM Users").fetchall()
        users = []
        for raw in usersRaw:
            if raw[0] != user:
                users.append(raw[0])
        print(users)
        return render(request, 'home.html', {'users': users, 'username': user, 'balance': balance})
    else:
        return redirect('transfer/')
