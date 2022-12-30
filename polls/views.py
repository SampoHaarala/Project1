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
        response = cur.execute("SELECT name FROM Users WHERE password='%s'" % (passw)).fetchone()
        if response == None:
            return redirect('/')
        print(response)
        if response == usern:
            return redirect('account/' + usern)
        else:
            return redirect('/')
    return render(request, 'login.html')

def transfer(request, user):
    if request.method == 'POST':
        to = request.POST.get('to')
        amount = request.POST.get('amount')
        if amount != None and to != None:
            amount = int(amount)
            con = sqlite3.connect('users.sqlite3')
            cur = con.cursor()
            balanceS = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (user)).fetchone()[0]
            print(balanceS)
            balanceT = cur.execute("SELECT balance FROM Users WHERE name='%s'" % (to)).fetchone()[0]
            print(balanceT)

        #Transfering minus amounts causes the sender to receive
            balanceS -= amount
            balanceT += amount

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
