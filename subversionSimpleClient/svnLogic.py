#! /usr/bin/python

import pysvn
import time

class SvnLogHelper(object):
    
    def __init__(self):
        self.revision_number = 0
        self.author = ""
        self.time = ""
        self.message = ""
        self.changed_paths = ""
        self.files = {}
        
class SvnLogPathHelper(object):
    
    def __init__(self):
        self.action = ""
        self.path = ""
        self.copyfrom_path = ""
        self.copyfrom_revision = 0
        
    def __str__(self):
        return "{0} - {1} | {2} - {3}".format(self.action, self.path, self.copyfrom_path, self.copyfrom_revision)
        
        
        

class SvnLogic(object):
    
    def __init__(self):
        self.version = "0.0.1"
        self.client = pysvn.Client()
        
    def svnStatus(self, path):
        #client = pysvn.Client()
        files_changes = self.client.status(path)
        dictionary_changes = {}
        added = []
        deleted = []
        modified = []
        conflicted = []
        unversioned = []
        for f in files_changes:
            if f.text_status == pysvn.wc_status_kind.added:
                added.append(f.path)
            elif f.text_status == pysvn.wc_status_kind.deleted:
                deleted.append(f.path)
            elif f.text_status == pysvn.wc_status_kind.modified:
                modified.append(f.path)
            elif f.text_status == pysvn.wc_status_kind.conflicted:
                conflicted.append(f.path)                
            elif f.text_status == pysvn.wc_status_kind.unversioned:
                unversioned.append(f.path)
            
        dictionary_changes['added'] = added
        dictionary_changes['deleted'] = deleted
        dictionary_changes['modified'] = modified
        dictionary_changes['conflicted'] = conflicted
        dictionary_changes['unversioned'] = unversioned
        return dictionary_changes
    
    """ 
    The default is to stop on copy.
    """
    def svnLog(self, path, stopOnCopy = True):
        entry = self.client.info(path)
        global_url = entry.url
        head = entry.revision.number
        logs = None
        if stopOnCopy:
            logs = self.client.log(global_url)
        else:
            print global_url
            #entry = self.client.info(global_url)
            working_copy_revision = entry.revision.number
            start = pysvn.Revision(pysvn.opt_revision_kind.number, working_copy_revision)
            end = pysvn.Revision(pysvn.opt_revision_kind.number, 0)
            logs = self.client.log(path, start, end, True, True, 0)
            head = entry.revision.number
        
        #print logs
        
        return_list = []
        for info in logs:
            #print info
            helper = SvnLogHelper()
            helper.revision_number = info.revision.number
            helper.author = info.author
            helper.time = time.ctime(info.date)
            helper.message = info.message
            #print info.changed_paths
            #helper.changed_paths = info.changed_paths
            changed_paths = []
            #print "=================="
            for cha in info.changed_paths:
                #print cha.__dict__
                if cha.copyfrom_revision != None:
                    changedPathHelper = SvnLogPathHelper()
                    changedPathHelper.action = cha.action
                    changedPathHelper.path = cha.path
                    changedPathHelper.copyfrom_path = cha.copyfrom_path
                    changedPathHelper.copyfrom_revision = cha.copyfrom_revision.number
                    changed_paths.append(changedPathHelper)
            helper.changed_paths = changed_paths
            #print "=================="
            #print info.revision.number
            #print info.author
            #print time.ctime(info.date)
            #print info.message
            #print info.changed_paths
            #print "====== Files ======="
#            if head != None:
#                helper.files = self.svnDiffSummarize(path, head, path, info.revision.number)
#            head = info.revision.number
            return_list.append(helper)
        #print return_list
        my_reversed = reversed(return_list)    
        #print my_reversed
        last = 0
        aux_return_list = []
        for auxHelp in my_reversed:
            if last != 0:
                auxHelp.files = self.svnDiffSummarize(path, auxHelp.revision_number, path, last)
            last = auxHelp.revision_number
            #print auxHelp.files
        #print my_reversed
        return return_list
            
    def svnDiffSummarize(self, path1, revision1, path2, revision2):
        head = pysvn.Revision(pysvn.opt_revision_kind.number, revision1)
        end = pysvn.Revision(pysvn.opt_revision_kind.number, revision2)
        
        added = []
        deleted = []
        modified = []
        prop_changed = []
        nothing = []
        files = self.client.diff_summarize(path1, head, path2, end)
        for info in files:
            path = info.path
            if info.node_kind == pysvn.node_kind.dir:
                path += '/'
            if info.summarize_kind == pysvn.diff_summarize_kind.normal:
                nothing.append(path)
            elif info.summarize_kind == pysvn.diff_summarize_kind.modified:
                modified.append(path)
            elif info.summarize_kind == pysvn.diff_summarize_kind.delete:
                deleted.append(path)
            elif info.summarize_kind == pysvn.diff_summarize_kind.added:
                added.append(path)
            elif info.prop_changed:
                prop_changed.append(path)
                
        dictionary_changes = {}
        dictionary_changes['added'] = added
        dictionary_changes['deleted'] = deleted
        dictionary_changes['modified'] = modified
        dictionary_changes['nothing'] = nothing
        dictionary_changes['prop_changed'] = prop_changed
        return dictionary_changes

