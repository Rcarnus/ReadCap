#!/usr/bin/env python

import os
from collections import OrderedDict
from moulinette_Types import *
from moulinette_Components import *

capdir = ""
outputdir = "./output/"


def output(dirname):
	if not os.path.exists(dirname):
		os.mkdir(dirname)
	if not os.path.isdir(dirname):
		raise TypeError("Output directory aleady exists as file")
	print "output placed in: " + dirname
	"""
	ClassFile {
	    u4             magic;
	    u2             minor_version;
	    u2             major_version;
	    u2             constant_pool_count;
	    cp_info        constant_pool[constant_pool_count-1];
	    u2             access_flags;
	    u2             this_class;
	    u2             super_class;
	    u2             interfaces_count;
	    u2             interfaces[interfaces_count];
	    u2             fields_count;
	    field_info     fields[fields_count];
	    u2             methods_count;
	    method_info    methods[methods_count];
	    u2             attributes_count;
	    attribute_info attributes[attributes_count];
	}
	"""
	print "done"

def represent(dico,profondeur):
	for elem in dico.iterkeys():
		if type(dico[elem]) is str:
			print profondeur*'\t'+elem+": "+str(dico[elem]).encode('hex')
		elif type(dico[elem]) is int:
			print profondeur*'\t'+elem+": "+str(dico[elem])
		elif type(dico[elem]) is OrderedDict:
			print profondeur*'\t'+elem+":"
			represent(dico[elem],profondeur+1)
		elif type(dico[elem]) is list:
			print profondeur*'\t'+elem+":"
			for el in dico[elem]:
				represent(el,profondeur+1)
				print ""
		elif type(dico[elem]) is AID:
			print profondeur*'\t'+str(dico[elem])
			print profondeur*'\t'+dico[elem].resolve()
		elif type(dico[elem]) is ConstantPoolTag:
			print profondeur*'\t'+elem+": (" + str(dico[elem]) + ") " + dico[elem].resolve()
		elif type(dico[elem]) is ClsAccessFlags or type(dico[elem]) is MethodAccessFlags \
				or type(dico[elem]) is FieldAccessFlags \
				or type(dico[elem]) is ClassBitField:
			print profondeur*'\t'+elem+": (" + str(dico[elem]) + ") " + dico[elem].resolve()
		else:
			print type(dico[elem])
			raise TypeError("Unhandled type for element to represent")

if __name__ == "__main__":

	
	
	header = Header(capdir)
	directory = Directory(capdir)
	applet = Applet(capdir)
	imports = Import(capdir)
	classes = Classes(capdir)
	constant_pool = ConstantPool(capdir)
	methods = Methods(capdir)
	descriptor = Descriptor(capdir)
	static_fields = StaticFields(capdir)
	print "======Header======="
	represent(header.fields,0)
	print "\n=====Directory======"
	represent(directory.fields,0)
	print "\n=====Applet======"
	represent(applet.fields,0)
	print "\n=====Imports======"
	represent(imports.fields,0)
	print "\n=====Classes======"
	represent(classes.fields,0)
	print "\n=====Methods======"
	represent(methods.fields,0)
	print "\n=====Descriptor======"
	represent(descriptor.fields,0)
	print "\n=====ConstantPool======"
	represent(constant_pool.fields,0)
	print "\n=====StaticField======"
	represent(static_fields.fields,0)

	#output(dirname)
