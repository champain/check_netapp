from NetApp.NaServer import *

class GetCounters():
    def __init__(self, na_object):
	self.na_object = na_object
        # Start out by building the xml necessary for the request
        self.get_counters = NaElement("perf-object-counter-list-info")
        self.get_counters.child_add_string("objectname", self.na_object)
        self.get_counters.sprintf()
        # Invoke the server
        self.counters_out = server.invoke_elem(self.get_counters)
        # Lot of shit to walk down here
        self.counters_list = self.counters_out.children_get()

    def getOut(self):
	self.count_dict = {}
        for self.i in self.counters_list:
            self.counter_info = self.i.children_get()
            for self.count in self.counter_info:
       	        self.count_desc = self.count.child_get_string("desc")
       	        self.count_name = self.count.child_get_string("name")
       	        self.count_unit = self.count.child_get_string("unit")
   		self.count_list = [self.count_desc, self.count_unit]
       	        self.count_dict[self.count_name] = self.count_list
	    return self.count_dict

# Let's gather all the counters for perf_objects
class GetAllObj():
    def __initi__(self):
	return None
   	# Function to gather all performance objects into one array	
    def getList(self):
        # Very simple API call here
        self.get_obj = NaElement("perf-object-list-info")
    
        # Invoke the server
        self.obj_out = server.invoke_elem(self.get_obj)
        self.obj_out.sprintf()
    
        # Walk down the xml
        self.obj_list = self.obj_out.children_get()
        self.obj_name_list = []
	for self.i in self.obj_list:
            self.obj_info = self.i.children_get()
            for self.obj in self.obj_info:
                self.obj_name = self.obj.child_get_string("name")
                self.obj_name_list.append(self.obj_name)
        return self.obj_name_list



# Now let's create a function that takes each dictionary and spits out
# Actual data we can use

def na_parse(obj_dict):
    good_list = []
    bad_list = []
    for x in obj_dict:
        if "none" in obj_dict[x][1] and "Total" in obj_dict[x][0]:
            good_list.append(x)
        elif "none" in obj_dict[x][1] and "number" in obj_dict[x][0]:
            good_list.append(x)
        elif "none" in obj_dict[x][1]:
            bad_list.append(x)
        else:
            good_list.append(x)
    return good_list

server = NaServer('localhost', 1, 21)
# Only used for testing
server.set_port(443)
user = 'arinapi'
pw = 'thisthang'
# Basic server details
server.set_transport_type('HTTPS')
server.set_style('LOGIN')
server.set_admin_user(user, pw)


# Define a main function, more 'pythonicly'
if __name__ == "__main__":
    final_dict = {}
    the_app = GetAllObj()
    for i in the_app.getList():
        next_app = GetCounters(i)
        final_list = na_parse(next_app.getOut())
        final_dict[i] = final_list
    print final_dict
