# -*- coding: UTF-8 -*-
#__author__ = 'li90.com'
import os, sys, yaml
import salt, salt.client, salt.output#salt.output.highstate
import re,argparse
##########################################################
# 说明:
# 1 master.d目录下必须定义项目的发布机信息
#  projects:
#    bbs_wwwroot1:
#      release_id: 'SN-linux-release'
# 2 发布机、线上生产机的minion.d目录下必须定义的grains信息
#  grains:
#    project:
#      - bbs_wwwroot1
# 3 其他信息
# pillar变量定义
#   1) 以项目名为各项目的pillar.sls名
#   2) sls文件中info信息严格按照模版,key可增加,但不能改变
#      数据类型也严格保持,由其dict list
##########################################################
##########################################################
# 以下是本脚本配置参数:
##########################################################
file_roots='/salt_home/salt'
pillar_roots='/salt_home/pillar'
##########################################################
def inputtopsls(project):
    '''
    修改pillar top.sls 文件,决定pillar变量推送target
    '''
    projectname="project:%s" % project
    data={'base': {projectname: [{'match': 'grain'}, project]}}
    pillartopfile="%s/top.sls" % pillar_roots
    fw = open(pillartopfile, 'w')
    yaml.dump(data, fw)
    fw.close()
def modifyrollbacksls(version_no):
    '''
    修改rollback.sls 文件中的版本号,决定回滚到具体版本
    '''
    rollbackfile="%s/rollback.sls" % file_roots
    fr = open(rollbackfile, 'r')
    x = yaml.load(fr)
    data = x
    fr.close()
    tmpvalue='{{ pillar["info"]["releasenode"]["projecthome"] }}' + version_no
    data['isexists']['file.exists'][0]['name']=tmpvalue
    data['link_to_currentdir']['file.symlink'][1]['target']=tmpvalue
    fw = open(rollbackfile, 'w')
    yaml.dump(data, fw)
    fw.close()
class SaltStack:
    def __init__(self, project):
        try:
            self.client=salt.client.LocalClient()
        except Exception,e:
            print(e.__class__, e)
            sys.exit()
        self.project=project
        self.projectstr="project:%s" % self.project
        #load master args
        self.__opts__ = salt.config.client_config('/etc/salt/master')
        try:
          self.release_id=self.__opts__['projects'][self.project]['release_id']
        except Exception,e:
            print(e.__class__, e)
            sys.exit()
        #各种信息刷新
        ret=self.client.cmd(self.projectstr, 'saltutil.sync_all', expr_form='grain')
        salt.output.display_output(ret, '', self.__opts__)
        ret=self.client.cmd(self.projectstr, 'sys.reload_modules', expr_form='grain')
        salt.output.display_output(ret, '', self.__opts__)
        ret=self.client.cmd(self.projectstr, 'saltutil.refresh_modules', expr_form='grain')
        salt.output.display_output(ret, '', self.__opts__)
        ret=self.client.cmd(self.projectstr, 'saltutil.refresh_pillar', expr_form='grain')
        salt.output.display_output(ret, '', self.__opts__)
        #从release主机过得pillar变量
        ret=self.client.cmd(self.release_id, 'pillar.data')
        self.__pillar__=ret[self.release_id]
    def execstate(self, task, hostid=''):
        '''
        直接调用state.sls 
        '''
        if not hostid:hostid=self.release_id
        ret=self.client.cmd(hostid, 'state.sls', [task])
        salt.output.display_output(ret, 'highstate', self.__opts__)
    def RollBack(self):
        '''
        交互输入版本号,进入调用state.sls
        '''
        version_no=raw_input("请正确输入你的版本号: ").strip()
        modifyrollbacksls(version_no)
        self.execstate('rollback')
    def RsyncToProd(self):
        '''
        rsunc 推送代码上线，不兼容windows
        '''
        src="%s%s/" % (self.__pillar__['info']['releasenode']['projecthome'], \
                       self.__pillar__['info']['releasenode']['currentdir']\
                      )
        delete="delete=%s" % self.__pillar__['info']['rsync']['delete']
        update="update=%s" % self.__pillar__['info']['rsync']['update']
        passwordfile="passwordfile=%s" % self.__pillar__['info']['rsync']['passwordfile']
        excludefrom="excludefrom=%s%s" % (self.__pillar__['info']['releasenode']['projecthome'], \
                                          self.__pillar__['info']['rsync']['excludefrom']\
                                         )
        for nodedata in self.__pillar__['info']['prodnode']:
            print "%s:\t%s" % (nodedata['id'], nodedata['ip'])
            dst="%s::%s" % (nodedata['ip'], \
                            nodedata['projecthome'].replace(self.__pillar__['info']['rsync']['rootdir'], \
                                                            self.__pillar__['info']['rsync']['rootname']\
                                                           )\
                           )
            ret=self.client.cmd(self.release_id,\
                                'rsync.rsync',\
                                [src, dst, delete, update, passwordfile, excludefrom]\
                               )
            salt.output.display_output(ret, '', self.__opts__)
    def FlushConfig(self):
        '''
        对生产环境更新配置
        '''
        for nodedata in self.__pillar__['info']['prodnode']:
            self.execstate('config', nodedata['id'])


#############################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='You can start publishing program.')
    parser.add_argument('-x', dest='eXec',nargs='+')
    parser.add_argument('-o', dest='Objects',nargs='+')
    args = parser.parse_args()
    EXEC=args.eXec[0]
    project=args.Objects[0]
    inputtopsls(project)
    n=SaltStack(project)
    if EXEC=='release':
        n.execstate('release')
    elif EXEC=='prod':
        n.RsyncToProd()
    elif EXEC=='config':
        n.FlushConfig()
    elif EXEC=='rollback':
        n.RollBack()
    elif EXEC=='show':
        n.execstate('showversion')
    else:
        print '这不是一个正确的操作对象'
