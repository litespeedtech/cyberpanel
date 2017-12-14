# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import hashlib
import json

from django.shortcuts import render,redirect
from django.http import HttpResponse
from models import Users
from loginSystem.models import Administrator
import plogical.CyberCPLogFileWriter as logging
from loginSystem.views import loadLoginPage
from websiteFunctions.models import Websites
from websiteFunctions.models import ChildDomains
import pwd
import grp
import subprocess
from plogical.virtualHostUtilities import virtualHostUtilities
import shlex
# Create your views here.

def loadFTPHome(request):
    try:
        val = request.session['userID']
        return render(request,'ftp/index.html')
    except KeyError:
        return redirect(loadLoginPage)


def createFTPAccount(request):
    try:
        val = request.session['userID']
        try:
            admin = Administrator.objects.get(pk=request.session['userID'])

            if admin.type == 1:
                websites = Websites.objects.all()
                websitesName = []

                for items in websites:
                    websitesName.append(items.domain)
            else:
                if admin.type == 2:
                    websites = Websites.objects.filter(admin=admin)
                    admins = Administrator.objects.filter(owner=admin.pk)
                    websitesName = []

                    for items in websites:
                        websitesName.append(items.domain)

                    for items in admins:
                        webs = Websites.objects.filter(admin=items)

                        for web in webs:
                            websitesName.append(web.domain)
                else:
                    websitesName = []
                    websites = Websites.objects.filter(admin=admin)
                    for items in websites:
                        websitesName.append(items.domain)

            return render(request, 'ftp/createFTPAccount.html', {'websiteList':websitesName,'admin':admin.userName})
        except BaseException, msg:
            logging.CyberCPLogFileWriter.writeToFile(str(msg))
            return HttpResponse(str(msg))

    except KeyError:
        return redirect(loadLoginPage)


def submitFTPCreation(request):
    try:
        val = request.session['userID']
        try:
            if request.method == 'POST':



                data = json.loads(request.body)
                userName = data['ftpUserName']
                password = data['ftpPassword']
                path = data['path']

                ## need to get gid and uid

                try:
                    website = ChildDomains.objects.get(domain=data['ftpDomain'])
                    externalApp = website.master.externalApp
                except:
                    website = Websites.objects.get(domain=data['ftpDomain'])
                    externalApp = website.externalApp

                uid = pwd.getpwnam(externalApp).pw_uid
                gid = grp.getgrnam(externalApp).gr_gid

                ## gid , uid ends

                path = path.lstrip("/")

                if len(path)>0:

                    path = "/home/" + data['ftpDomain']+"/public_html/"+path

                    execPath = "sudo python " + virtualHostUtilities.cyberPanel + "/plogical/ftpUtilities.py"

                    execPath = execPath + " ftpFunctions --path " + path + " --externalApp " + externalApp



                    output = subprocess.check_output(shlex.split(execPath))

                    if output.find("1,None") > -1:
                        pass
                    else:
                        data_ret = {'creatFTPStatus': 0, 'error_message': "Not able to create the directory specified, for more information see CyberPanel main log file."}
                        json_data = json.dumps(data_ret)
                        return HttpResponse(json_data)

                else:
                    path = "/home/" + data['ftpDomain']


                hash = hashlib.md5()
                hash.update(password)

                admin = Administrator.objects.get(pk=request.session['userID'])

                userName = admin.userName + "_" + userName

                if website.package.ftpAccounts == 0:
                    user = Users(domain=website, user=userName, password=hash.hexdigest(), uid=uid, gid=gid, dir=path,
                                 quotasize=website.package.diskSpace,
                                 status="1",
                                 ulbandwidth=500000,
                                 dlbandwidth=500000,
                                 date=datetime.now())

                    user.save()



                    data_ret = {'creatFTPStatus': 1, 'error_message': "None"}
                    json_data = json.dumps(data_ret)
                    return HttpResponse(json_data)

                elif website.users_set.all().count() < website.package.ftpAccounts:
                    user = Users(domain=website,user=userName, password=hash.hexdigest(), uid=uid, gid=gid, dir=path, quotasize=website.package.diskSpace,
                                 status="1",
                                 ulbandwidth=500000,
                                 dlbandwidth=500000,
                                 date=datetime.now())

                    user.save()

                    data_ret = {'creatFTPStatus': 1,'error_message': "None"}
                    json_data = json.dumps(data_ret)
                    return HttpResponse(json_data)
                else:
                    data_ret = {'creatFTPStatus': 0, 'error_message': "Exceeded maximum amount of FTP accounts allowed for the package."}
                    json_data = json.dumps(data_ret)
                    return HttpResponse(json_data)

        except BaseException,msg:
            data_ret = {'creatFTPStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'creatFTPStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)


def deleteFTPAccount(request):
    try:
        val = request.session['userID']
        try:
            admin = Administrator.objects.get(pk=request.session['userID'])

            if admin.type == 1:
                websites = Websites.objects.all()
                websitesName = []

                for items in websites:
                    websitesName.append(items.domain)
            else:
                if admin.type == 2:
                    websites = admin.websites_set.all()
                    admins = Administrator.objects.filter(owner=admin.pk)
                    websitesName = []

                    for items in websites:
                        websitesName.append(items.domain)

                    for items in admins:
                        webs = items.websites_set.all()

                        for web in webs:
                            websitesName.append(web.domain)
                else:
                    websitesName = []
                    websites = Websites.objects.filter(admin=admin)
                    for items in websites:
                        websitesName.append(items.domain)

            return render(request, 'ftp/deleteFTPAccount.html', {'websiteList':websitesName})
        except BaseException, msg:
            logging.CyberCPLogFileWriter.writeToFile(str(msg))
            return HttpResponse(str(msg))

    except KeyError:
        return redirect(loadLoginPage)


def fetchFTPAccounts(request):
    try:
        val = request.session['userID']
        try:
            if request.method == 'POST':

                data = json.loads(request.body)
                domain = data['ftpDomain']

                website = Websites.objects.get(domain=domain)


                ftpAccounts = website.users_set.all()

                json_data = "["
                checker = 0

                for items in ftpAccounts:
                    dic = {"userName":items.user}

                    if checker == 0:
                        json_data = json_data + json.dumps(dic)
                        checker = 1
                    else:
                        json_data = json_data + ',' + json.dumps(dic)

                json_data = json_data + ']'
                final_json = json.dumps({'fetchStatus': 1, 'error_message': "None", "data": json_data})
                return HttpResponse(final_json)



        except BaseException,msg:
            data_ret = {'fetchStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'fetchStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)


def submitFTPDelete(request):
    try:
        val = request.session['userID']
        try:
            if request.method == 'POST':

                data = json.loads(request.body)
                ftpUserName = data['ftpUsername']

                ftp = Users.objects.get(user=ftpUserName)
                ftp.delete()

                final_json = json.dumps({'deleteStatus': 1, 'error_message': "None"})
                return HttpResponse(final_json)

        except BaseException,msg:
            data_ret = {'deleteStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'deleteStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)


def listFTPAccounts(request):
    try:
        val = request.session['userID']
        try:
            admin = Administrator.objects.get(pk=request.session['userID'])

            if admin.type == 1:
                websites = Websites.objects.all()
                websitesName = []

                for items in websites:
                    websitesName.append(items.domain)
            else:
                if admin.type == 2:
                    websites = admin.websites_set.all()
                    admins = Administrator.objects.filter(owner=admin.pk)
                    websitesName = []

                    for items in websites:
                        websitesName.append(items.domain)

                    for items in admins:
                        webs = items.websites_set.all()

                        for web in webs:
                            websitesName.append(web.domain)
                else:
                    websitesName = []
                    websites = Websites.objects.filter(admin=admin)
                    for items in websites:
                        websitesName.append(items.domain)

            return render(request, 'ftp/listFTPAccounts.html', {'websiteList':websitesName})
        except BaseException, msg:
            logging.CyberCPLogFileWriter.writeToFile(str(msg))
            return HttpResponse(str(msg))

    except KeyError:
        return redirect(loadLoginPage)


def getAllFTPAccounts(request):
    try:
        val = request.session['userID']
        try:
            if request.method == 'POST':


                data = json.loads(request.body)
                selectedDomain = data['selectedDomain']

                domain = Websites.objects.get(domain=selectedDomain)

                records = Users.objects.filter(domain=domain)

                json_data = "["
                checker = 0

                for items in records:
                    dic = {'id': items.id,
                           'user': items.user,
                           'dir': items.dir,
                           'quotasize': str(items.quotasize)+"MB",
                           }

                    if checker == 0:
                        json_data = json_data + json.dumps(dic)
                        checker = 1
                    else:
                        json_data = json_data + ',' + json.dumps(dic)


                json_data = json_data + ']'
                final_json = json.dumps({'fetchStatus': 1, 'error_message': "None","data":json_data})
                return HttpResponse(final_json)

        except BaseException,msg:
            final_dic = {'fetchStatus': 0, 'error_message': str(msg)}
            final_json = json.dumps(final_dic)

            return HttpResponse(final_json)
    except KeyError:
        final_dic = {'fetchStatus': 0, 'error_message': "Not Logged In, please refresh the page or login again."}
        final_json = json.dumps(final_dic)
        return HttpResponse(final_json)


def changePassword(request):
    try:
        val = request.session['userID']
        try:
            if request.method == 'POST':



                data = json.loads(request.body)
                userName = data['ftpUserName']
                password = data['ftpPassword']


                hash = hashlib.md5()
                hash.update(password)

                admin = Administrator.objects.get(pk=request.session['userID'])

                ftp = Users.objects.get(user=userName)
                ftp.password = hash.hexdigest()
                ftp.save()

                data_ret = {'changePasswordStatus': 1, 'error_message': "None"}
                json_data = json.dumps(data_ret)
                return HttpResponse(json_data)

        except BaseException,msg:
            data_ret = {'changePasswordStatus': 0, 'error_message': str(msg)}
            json_data = json.dumps(data_ret)
            return HttpResponse(json_data)
    except KeyError,msg:
        data_ret = {'changePasswordStatus': 0, 'error_message': str(msg)}
        json_data = json.dumps(data_ret)
        return HttpResponse(json_data)