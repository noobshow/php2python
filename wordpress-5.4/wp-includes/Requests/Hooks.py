#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// Handles adding and dispatching events
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// Handles adding and dispatching events
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_Hooks(Requests_Hooker):
    #// 
    #// Registered callbacks for each hook
    #// 
    #// @var array
    #//
    hooks = Array()
    #// 
    #// Constructor
    #//
    def __init__(self):
        
        
        pass
    # end def __init__
    #// 
    #// Register a callback for a hook
    #// 
    #// @param string $hook Hook name
    #// @param callback $callback Function/method to call on event
    #// @param int $priority Priority number. <0 is executed earlier, >0 is executed later
    #//
    def register(self, hook_=None, callback_=None, priority_=0):
        
        
        if (not (php_isset(lambda : self.hooks[hook_]))):
            self.hooks[hook_] = Array()
        # end if
        if (not (php_isset(lambda : self.hooks[hook_][priority_]))):
            self.hooks[hook_][priority_] = Array()
        # end if
        self.hooks[hook_][priority_][-1] = callback_
    # end def register
    #// 
    #// Dispatch a message
    #// 
    #// @param string $hook Hook name
    #// @param array $parameters Parameters to pass to callbacks
    #// @return boolean Successfulness
    #//
    def dispatch(self, hook_=None, parameters_=None):
        if parameters_ is None:
            parameters_ = Array()
        # end if
        
        if php_empty(lambda : self.hooks[hook_]):
            return False
        # end if
        for priority_,hooked_ in self.hooks[hook_].items():
            for callback_ in hooked_:
                call_user_func_array(callback_, parameters_)
            # end for
        # end for
        return True
    # end def dispatch
# end class Requests_Hooks
