from django.conf.urls import url
import views

urlpatterns = [
    url(r'^securityHome', views.securityHome, name='securityHome'),
    url(r'^$', views.firewallHome, name='firewallHome'),
    url(r'^getCurrentRules', views.getCurrentRules, name='getCurrentRules'),
    url(r'^addRule', views.addRule, name='addRule'),
    url(r'^deleteRule', views.deleteRule, name='deleteRule'),


    url(r'^reloadFirewall', views.reloadFirewall, name='reloadFirewall'),
    url(r'^stopFirewall', views.stopFirewall, name='stopFirewall'),
    url(r'^startFirewall', views.startFirewall, name='startFirewall'),
    url(r'^firewallStatus', views.firewallStatus, name='firewallStatus'),

    ## secure SSH

    url(r'^secureSSH', views.secureSSH, name='secureSSH'),
    url(r'^getSSHConfigs', views.getSSHConfigs, name='getSSHConfigs'),

    url(r'^saveSSHConfigs', views.saveSSHConfigs, name='saveSSHConfigs'),

    url(r'^deleteSSHKey', views.deleteSSHKey, name='deleteSSHKey'),

    url(r'^addSSHKey', views.addSSHKey, name='addSSHKey'),
]