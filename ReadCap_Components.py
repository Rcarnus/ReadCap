#!/usr/bin/env python

from collections import OrderedDict
from moulinette_Types import *




class Classes(object):
    def __init__(self,capdir):
        self.parse_class(capdir)

    def parse_class(self,capdir):
        """
        class_component {
             u1 tag 
             u2 size 
             u2 signature_pool_length 
             type_descriptor signature_pool[] 
             interface_info interfaces[] 
             class_info classes[] 
        }
        """
        classes = OrderedDict()
        classes_file = open(capdir+"Class.cap","rb")
        classes['tag'] = classes_file.read(1)
        classes['size'] = classes_file.read(2)
        #classes['signature_pool_length'] = classes_file.read(2)
        """
        type_descriptor { 
            u1 nibble_count;  
            u1 type[(nibble_count+1) / 2]; 
        }
        """
        
        """
        if classes['signature_pool_length'] != '':
            signature_pool = []
            length = int(str(classes['signature_pool_length']).encode('hex'),16)
            while length > 0:
                desc = OrderedDict()
                desc['nibble_count'] = classes_file.read(1)
                print desc
                typelen = (ord(desc['nibble_count'])+1) / 2 #FIXME: why is this zero?
                print typelen
                return
                desc['type'] = classes_file.read(typelen)
                signature_pool.append(desc)
                length -= typelen + 1
            classes['signature_pool'] = signature_pool
        """
        classes['signature_pool'] = classes_file.read(12)


        """
        interface_info { 
            u1 bitfield { 
                 bit[4] flags 
                 bit[4] interface_count 
                 } 
            class_ref superinterfaces[interface_count] 
            interface_name_info interface_name5 
        } 

        class_info { 
                u1 bitfield { 
                 bit[4] flags 
                 bit[4] interface_count 
            } 
            class_ref super_class_ref 
            u1 declared_instance_size 
            u1 first_reference_token 
            u1 reference_count 
            u1 public_method_table_base 
            u1 public_method_table_count 
            u1 package_method_table_base 
            u1 package_method_table_count 
            u2 public_virtual_method_table[public_method_table_count] 
            u2 package_virtual_method_table[package_method_table_count] 
            implemented_interface_info interfaces[interface_count] 
            remote_interface_info remote_interfaces 6 

        }
        """
        class_list = []
        bitfield = classes_file.read(1)
        while (bitfield != ''):
            flag = ClassBitField(str(bitfield.encode('hex')[0]))
            if (flag.flags & 0x08) != 0:
                #interface
                interface_info = OrderedDict()
                interface_info['flags'] = flag
                interface_info['interface_count'] = int(str(bitfield.encode('hex')[1],16))
                class_list.append(interface_info)
            else:
                #class
                class_info = OrderedDict()
                class_info['flags'] = flag
                class_info['interface_count'] = int(str(bitfield.encode('hex')[1]),16)
                class_info['super_class_ref'] = classes_file.read(2)
                class_info['declared_instance_size'] = classes_file.read(1)
                class_info['first_reference_token'] = classes_file.read(1)
                class_info['reference_count'] = classes_file.read(1)
                class_info['public_method_table_base'] = classes_file.read(1)
                class_info['public_method_table_count'] = classes_file.read(1)
                class_info['package_method_table_base'] = classes_file.read(1)
                class_info['package_method_table_count'] = classes_file.read(1)

                public_method_table = []
                for i in range(ord(class_info['public_method_table_count'])):
                    public_method = OrderedDict()
                    public_method['index'] = classes_file.read(2)
                    public_method_table.append(public_method)
                class_info['public_method_table'] = public_method_table

                package_method_table = []
                for i in range(ord(class_info['package_method_table_count'])):
                    package_method = OrderedDict()
                    package_method['index'] = classes_file.read(2)
                    package_method_table.append(package_method)
                class_info['package_method_table'] = package_method_table
                class_list.append(class_info)

                implemented_interfaces = []
                for i in range(class_info['interface_count']):
                    """
                    implemented_interface_info { 
                       class_ref interface 
                       u1 count 
                       u1 index[count] 
                    } 
                    """
                    implemented_interface = OrderedDict()
                    implemented_interface['class_ref'] = classes_file.read(2)
                    implemented_interface['count'] = classes_file.read(1)
                    index_list = []
                    for i in range(ord(implemented_interface['count'])):
                        index = OrderedDict()
                        index['index'] = classes_file.read(1)
                        index_list.append(index)
                    implemented_interface['index'] = index_list
                    implemented_interfaces.append(implemented_interface)
                class_info['implemented_interfaces'] = implemented_interfaces

            bitfield = classes_file.read(1)
        classes['list'] = class_list
        self.fields = classes

class Descriptor(object):
    def __init__(self, capdir):
        self.parse_descriptor(capdir)

    def parse_descriptor(self,capdir):
        """
        descriptor_component {
             u1 tag
             u2 size
             u1 class_count
             class_descriptor_info classes[class_count]
             type_descriptor_info types
        }
        """
        descriptor = OrderedDict()
        descriptor_file = open(capdir+"Descriptor.cap","rb")
        descriptor['tag'] = descriptor_file.read(1)
        descriptor['size'] = descriptor_file.read(2)
        descriptor['class_count'] = descriptor_file.read(1)
        """
        class_descriptor_info { 
             u1 token 
             u1 access_flags
             class_ref this_class_ref
             u1 interface_count 
             u2 field_count 
             u2 method_count 
             class_ref interfaces [interface_count] 
             field_descriptor_info fields[field_count] 
             method_descriptor_info methods[method_count] 
        }
        """
        desc_classes = []
        descriptor['classes'] = desc_classes
        if descriptor['class_count'] != '':
            for i in range(ord(descriptor['class_count'])):
                descriptor_info = OrderedDict()
                desc_classes.append(descriptor_info)
                descriptor_info['token'] = descriptor_file.read(1)
                descriptor_info['access_flags'] = ClsAccessFlags(descriptor_file.read(1))
                """
                CONSTANT_Classref_info {
                     u1 tag
                     union {
                          u2 internal_class_ref
                          { u1 package_token
                           u1 class_token
                          } external_class_ref
                     } class_ref
                     u1 padding
                }
                """
                descriptor_info['this_class_ref'] = descriptor_file.read(2)
                descriptor_info['interface_count'] = descriptor_file.read(1)
                descriptor_info['field_count'] = descriptor_file.read(2)
                descriptor_info['method_count'] = descriptor_file.read(2)
                if descriptor_info['interface_count'] != '' or ord(descriptor_info['interface_count']) != 0:
                    desc_interfaces = []
                    for i in range(ord(descriptor_info['interface_count'])):
                        desc_interface = OrderedDict()
                        desc_interface['class_ref'] = descriptor_file.read(2)
                        desc_interfaces.append(desc_interface)
                    descriptor_info['interfaces'] = desc_interfaces
                """
                field_descriptor_info { 
                     u1 token 
                     u1 access_flags 
                     union { 
                          static_field_ref static_field 
                         { 
                            class_ref class 
                            u1 token 
                          } instance_field 
                     } field_ref 
                     union { 
                            u2 primitive_type 
                            u2 reference_type 
                     } type 
                }
                """
                if descriptor_info['field_count'] != '' or ord(descriptor_info['field_count']) != 0:
                    desc_fields = []
                    for i in range(int(str(descriptor_info['field_count']).encode('hex'),16)):
                        desc_field = OrderedDict()
                        desc_field['token'] = descriptor_file.read(1)
                        desc_field['access_flags'] = FieldAccessFlags(descriptor_file.read(1))
                        desc_field['field_ref'] = descriptor_file.read(3) #TODO: may be detailed
                        desc_field['type'] = descriptor_file.read(2)
                        desc_fields.append(desc_field)
                    descriptor_info['fields'] = desc_fields
                """
                method_descriptor_info { 
                     u1 token 
                     u1 access_flags 
                     u2 method_offset 
                     u2 type_offset 
                     u2 bytecode_count 
                     u2 exception_handler_count 
                     u2 exception_handler_index 
                }
                """
                if descriptor_info['method_count'] != '' or ord(descriptor_info['method_count']) != 0:
                    desc_methods = []
                    for i in range(int(str(descriptor_info['method_count']).encode('hex'),16)):
                        desc_method = OrderedDict()
                        desc_method['token'] = descriptor_file.read(1)
                        desc_method['access_flags'] = MethodAccessFlags(descriptor_file.read(1))
                        desc_method['method_offset'] = descriptor_file.read(2)
                        desc_method['type_offset'] = descriptor_file.read(2)
                        desc_method['bytecode_count'] = descriptor_file.read(2)
                        desc_method['exception_handler_count'] = descriptor_file.read(2)
                        desc_method['exception_handler_index'] = descriptor_file.read(2)
                        offset = int(str(desc_method['method_offset']).encode('hex'),16)
                        bytecount = int(str(desc_method['bytecode_count']).encode('hex'),16)
                        desc_method['method'] = resolve_method(capdir,offset,bytecount)
                        desc_methods.append(desc_method)
                    descriptor_info['methods'] = desc_methods
        """
        type_descriptor_info { 
             u2 constant_pool_count 
             u2 constant_pool_types[constant_pool_count] 
             type_descriptor type_desc[] 
        } 
        """
        type_desc_info = OrderedDict()
        type_desc_info['constant_pool_count'] = descriptor_file.read(2)
        if type_desc_info['constant_pool_count'] != '':
            constant_pool_types = []
            for i in range(int(str(type_desc_info['constant_pool_count']).encode('hex'),16)):
                constant_pool_type = OrderedDict()
                constant_pool_type['value'] = descriptor_file.read(2)
                constant_pool_types.append(constant_pool_type)
            type_desc_info['constant_pool_types'] = constant_pool_types
            type_descs = []
            """
            type_descriptor {
                u1 nibble_count;  
                u1 type[(nibble_count+1) / 2]; 
            }
            """
            while True:
                type_desc =OrderedDict()
                type_desc['nibble_count'] = descriptor_file.read(1)
                if type_desc['nibble_count'] != '':
                    type_desc['type'] = descriptor_file.read((ord(type_desc['nibble_count'])+1)/2)
                    type_descs.append(type_desc)
                else:
                    break
            type_desc_info['type_descriptor'] = type_descs
        descriptor['types'] = type_desc_info


        if descriptor_file.read(1) != '':
            raise IOError("still data to read in the file")

        self.fields = descriptor

class Header(object):
    def __init__(self, capdir):
        self.parse_header(capdir)

    def parse_header(self,capdir):
        """
        header_component { 
             u1 tag 
             u2 size 
             u4 magic 
             u1 minor_version 
             u1 major_version 
             u1 flags 
             package_info package 
             package_name_info package_name 
        }
        """
        header = OrderedDict()
        header_file = open(capdir+"Header.cap","rb")
        header['tag'] = header_file.read(1)
        header['size'] = header_file.read(2)
        header['magic'] = header_file.read(4)
        header['minor_version'] = header_file.read(1)
        header['major_version'] = header_file.read(1)
        header['flags'] = header_file.read(1)
        """
        package_info { 
         u1 minor_version 
         u1 major_version 
         u1 AID_length 
         u1 AID[AID_length] 
        }
        """
        package_info_h = OrderedDict()
        package_info_h['minor_version'] = header_file.read(1)
        package_info_h['major_version'] = header_file.read(1)
        package_info_h['AID_length'] = header_file.read(1)
        if package_info_h['AID_length'] != '':
            package_info_h['AID'] = AID(header_file.read(ord(package_info_h['AID_length'])))
            header['package_info'] = package_info_h #FIXME: il semble que cette structure soit overwritten plus loin
        """
        package_name_info { 
             u1 name_length 
             u1 name[name_length] 
        } 
        """
        package_name_info = OrderedDict()
        package_name_info['length'] = header_file.read(1)
        if package_name_info['length'] != '':
            package_name_info['name'] = header_file.read(ord(package_name_info['length']))
            header['package_name_info'] = package_name_info
        self.fields = header

class Directory(object):
    def __init__(self,capdir):
        self.parse_directory(capdir)

    def parse_directory(self,capdir):
        """
        directory_component { 
               u1 tag 
               u2 size 
               u2 component_sizes[12] 
               static_field_size_info static_field_size 
               u1 import_count 
               u1 applet_count 
               u1 custom_count 
               custom_component_info custom_components[custom_count] 
         } 
        """
        directory = OrderedDict()
        directory_file = open(capdir+"Directory.cap","rb")
        directory['tag'] = directory_file.read(1)
        directory['size'] = directory_file.read(2)
        directory['component_sizes'] = directory_file.read(12*2)
        """
        static_field_size_info { 
            u2 image_size 
            u2 array_init_count 
            u2 array_init_size 
        }
        """
        static_field_size = OrderedDict()
        static_field_size['image_size'] = directory_file.read(2)
        static_field_size['array_init_count'] = directory_file.read(2)
        static_field_size['array_init_size'] = directory_file.read(2)
        directory['static_field_size'] = static_field_size
        directory['import_count'] = directory_file.read(1)
        directory['applet_count'] = directory_file.read(1)
        directory['custom_count'] = directory_file.read(1)
        """
        custom_component_info { 
            u1 component_tag 
            u2 size 
            u1 AID_length 
            u1 AID[AID_length] 
        } 
        """
        custom_components = []
        if directory['custom_count'] != '':
            custom_count = ord(directory['custom_count'])
            if custom_count != 0:
                for i in range(custom_count):
                    custom_component = OrderedDict()
                    custom_component['component_tag'] = directory_file.read(1)
                    custom_component['size'] = directory_file.read(2)
                    custom_component['AID_length'] = directory_file.read(1)
                    custom_component['AID'] = AID(directory_file.read(ord(custom_component['AID_length'])))
                    custom_components.append(custom_component)
        self.fields = directory

class Applet(object):
    def __init__(self,capdir):
        self.parse_applet(capdir)

    def parse_applet(self,capdir):
        """
        applet_component { 
            u1 tag 
            u2 size 
            u1 count 
            { u1 AID_length 
             u1 AID[AID_length] 
             u2 install_method_offset 
            } applets[count] 
        } 
        """
        applet = OrderedDict()
        applet_file = open(capdir+"Applet.cap","rb")
        applet['tag'] = applet_file.read(1)
        applet['size'] = applet_file.read(2)
        applet['count'] = applet_file.read(1)
        if applet['count'] != '':
            applets = []
            for i in range(ord(applet['count'])):
                applet_el = OrderedDict()
                applet_el['AID_length'] = applet_file.read(1)
                if applet_el['AID_length'] != '':
                    applet_el['AID'] = AID(applet_file.read(ord(applet_el['AID_length'])))
                    applet_el['install_method_offset'] = applet_file.read(2)
                applets.append(applet_el)
            applet['applets'] = applets
        self.fields = applet

class Import(object):
    def __init__(self,capdir):
        self.parse_import(capdir)

    def parse_import(self,capdir):
        """
        import_component { 
             u1 tag 
             u2 size 
             u1 count 
             package_info packages[count] 
        }
        """
        imports = OrderedDict()
        imports_file = open(capdir+"Import.cap","rb")
        imports['tag'] = imports_file.read(1)
        imports['size'] = imports_file.read(2)
        imports['count'] = imports_file.read(1)
        """
        package_info { 
         u1 minor_version 
         u1 major_version 
         u1 AID_length 
         u1 AID[AID_length] 
        }
        """
        if imports['count'] != '':
            packages = []
            for i in range(ord(imports['count'])):
                package_info = OrderedDict()
                package_info['minor_version'] = imports_file.read(1)
                package_info['major_version'] = imports_file.read(1)
                package_info['AID_length'] = imports_file.read(1)
                if package_info['AID_length'] != '':
                    #package_info['AID'] = imports_file.read(ord(package_info['AID_length']))
                    package_info['AID'] = AID(imports_file.read(ord(package_info['AID_length'])))
                packages.append(package_info)
            imports['packages'] = packages
        self.fields = imports

class StaticFields(object):
    def __init__(self,capdir):
        self.parse_static_fields(capdir)

    def parse_static_fields(self,capdir):
        """
        static_field_component { 
         u1 tag 
         u2 size 
         u2 image_size 
         u2 reference_count 
         u2 array_init_count 
         array_init_info array_init[array_init_count] 
         u2 default_value_count 
         u2 non_default_value_count 
         u1 non_default_values[non_default_values_count] 
        } 
        """
        static_fields = OrderedDict()
        static_fields_file = open(capdir+"StaticField.cap","rb")
        static_fields['tag'] = static_fields_file.read(1)
        static_fields['size'] = static_fields_file.read(2)
        static_fields['image_size'] = static_fields_file.read(2)
        static_fields['reference_count'] = static_fields_file.read(2)
        static_fields['array_init_count'] = static_fields_file.read(2)

        array_init = []
        """
          array_init_info { 
                u1 type 
                u2 count 
                u1 values[count] 
          } 
        """
        for i in range(int(str(static_fields['array_init_count']).encode('hex'),16)):
            array_init_info = OrderedDict()
            array_init_info['type'] = static_fields_file.read(1)
            array_init_info['count'] = static_fields_file.read(2)
            array_init_info['values'] = static_fields_file.read(int(str(array_init_info['count']).encode('hex'),16))
            array_init.append(array_init_info)
        static_fields['array_init'] = array_init

        static_fields['default_value_count'] = static_fields_file.read(2)
        static_fields['non_default_value_count'] = static_fields_file.read(2)
        static_fields['non_default_values'] = static_fields_file.read(int(str(static_fields['non_default_value_count']).encode('hex'),16))
        self.fields = static_fields

class ConstantPool(object):
    def __init__(self,capdir):
        self.parse_constant_pool(capdir)

    def parse_constant_pool(self,capdir):
        """
        constant_pool_component { 
              u1 tag 
              u2 size 
              u2 count 
              cp_info constant_pool[count]
        }
        """
        constant_pool = OrderedDict()
        constant_pool_file = open(capdir+"ConstantPool.cap","rb")
        constant_pool['tag'] = constant_pool_file.read(1)
        constant_pool['size'] = constant_pool_file.read(2)
        constant_pool['count'] = constant_pool_file.read(2)
        """
        cp_info { 
           u1 tag 
           u1 info[3] 
        }
        """
        if constant_pool['count'] != '':
            constant_pool_list = []
            for i in range(int(str(constant_pool['count']).encode('hex'),16)):
                constant_pool_el = OrderedDict()
                constant_pool_el['tag'] = ConstantPoolTag(constant_pool_file.read(1))
                constant_pool_el['info'] = constant_pool_file.read(3)
                constant_pool_list.append(constant_pool_el)
            constant_pool['constant_pool'] = constant_pool_list
        self.fields = constant_pool

class Methods(object):
    def __init__(self,capdir):
        self.parse_methods(capdir)
    
    def parse_methods(self,capdir):
        """
        method_component {
             u1 tag
             u2 size
             u1 handler_count
             exception_handler_info exception_handlers[handler_count]
             method_info methods[]
        }
        """
        methods = OrderedDict()
        methods_file = open(capdir+"Method.cap","rb")
        methods['tag'] = methods_file.read(1)
        methods['size'] = methods_file.read(2)
        methods['handler_count'] = methods_file.read(1)
        """
        exception_handler_info {
             u2 start_offset
             u2 bitfield {
                  bit[1] stop_bit
                  bit[15] active_length
             }
             u2 handler_offset
             u2 catch_type_index
        }
        """
        if methods['handler_count'] != '':
            exception_handlers = []
            for i in range(ord(methods['handler_count'])):
                exception_handler = OrderedDict()
                exception_handler['start_offset'] = methods_file.read(2)
                exception_handler['bitfield'] = methods_file.read(2)
                exception_handler['handler_offset'] = methods_file.read(2)
                exception_handler['catch_type_index'] = methods_file.read(2)
                exception_handlers.append(exception_handler)
            methods['exception_handlers'] = exception_handlers
        """
        method_info { 
             method_header_info method_header 
             u1 bytecodes[] 
        } 
        """
        method_list = []
        methods['methods'] = method_list
        methods['bytecode'] = methods_file.read()
        methods_file.close()
        self.fields = methods

def resolve_method(capdir,offset,bytecount):
    """
    offset is an int
    bytecount is an int

    returns a method_info structure
    """
    if bytecount == 0:
        return ""
    """
    method_info { 
         method_header_info method_header 
         u1 bytecodes[] 
    }


    method_header_info { 
         u1 bitfield { 
             bit[4] flags 
             bit[4] max_stack 
        } 
        u1 bitfield { 
             bit[4] nargs 
             bit[4] max_locals 
        } 
    } 
    """
    methods_file = open(capdir+"Method.cap","rb")
    bytestream = methods_file.read()
    methods_file.close()
    realoffset = offset + 3 #We skip the header of the Method Component (starting at the exception_handler list)
    flags = int(str(bytestream[realoffset]).encode('hex')[0])
    method_info = OrderedDict()
    method_hdr = OrderedDict()
    method_info['method_header'] = method_hdr
    #normal
    if (flags & 0x8) > 0:
        """
        extended_method_header_info { 
            u1 bitfield { 
              bit[4] flags 
              bit[4] padding 
            } 
            u1 max_stack 
            u1 nargs 
            u1 max_locals 
        } 
        """
        method_hdr["flags"] = int(str(bytestream[realoffset]).encode('hex')[0],16)
        method_hdr["max_stack"] = int(str(bytestream[realoffset+1]).encode('hex'),16)
        method_hdr["nargs"] = int(str(bytestream[realoffset+2]).encode('hex'),16)
        method_hdr["max_locals"] = int(str(bytestream[realoffset+3]).encode('hex'),16)
        start = realoffset+4
        end = start + bytecount
        method_info['bytecode'] = bytestream[start:end]
        return method_info
    #abstract
    elif (flags & 0x4) > 0:
        print "abstract"
        return method_info
    else:
        """
        method_header_info { 
             u1 bitfield { 
                 bit[4] flags 
                 bit[4] max_stack 
            } 
            u1 bitfield { 
                 bit[4] nargs 
                 bit[4] max_locals 
            } 
        } 
        """
        method_hdr["flags"] = int(str(bytestream[realoffset]).encode('hex')[0],16)
        method_hdr["max_stack"] = int(str(bytestream[realoffset]).encode('hex')[1],16)
        method_hdr["nargs"] = int(str(bytestream[realoffset+1]).encode('hex')[0],16)
        method_hdr["nargs"] = int(str(bytestream[realoffset+1]).encode('hex')[1],16)
        start = realoffset+2
        end = start + bytecount
        method_info['bytecode'] = bytestream[start:end]
        return method_info
