
class AID(object):
    def __init__(self, bytestream):
        #print bytestream
        self.rid = bytestream[:5]
        self.pix = bytestream[5:]

    def __repr__(self):
        return "< AID Instance rid:" + str(self.rid).encode('hex') + " pix:" + str(self.pix).encode('hex') + " >"

    def __str__(self):
        #return str(self.rid) + " | " + str(self.pix)
        return str(self.rid).encode('hex') + " | " + str(self.pix).encode('hex')

    def resolve(self):
        if str(self.rid).encode('hex') == "a000000062":
            return "javacard.framework.?"
        elif str(self.rid).encode('hex') == "a000000009":
            if str(self.pix).encode('hex') == "0005ffffffff8912000000":
                return "uicc.toolkit (ETSI)"
            elif str(self.pix).encode('hex') == "0005ffffffff8911000000":
                return "uicc.access (ETSI)"
            else:
                return "unknown (ETSI)"
        else:
            return "Another unknown component"

class ClsAccessFlags(object):
    def __init__(self, flags):
        self.flags = ord(flags)

    def __repr__(self):
        return "< ClsAccessFlags Instance value:" + str(self.flags).encode('hex') + " >"

    def __str__(self):
        #return str(self.rid) + " | " + str(self.pix)
        return hex(self.flags)

    def resolve(self):
        attributes = ""
        if (self.flags & 0x01) != 0:
            attributes += " public"
        if (self.flags & 0x10) != 0:
            attributes += " final"
        if (self.flags & 0x40) != 0:
            attributes += " interface"
        if (self.flags & 0x80) != 0:
            attributes += " abstract"
        return attributes

class MethodAccessFlags(object):
    def __init__(self, flags):
        self.flags = ord(flags)

    def __repr__(self):
        return "< MethodAccessFlags Instance value:" + str(self.flags).encode('hex') + " >"

    def __str__(self):
        #return str(self.rid) + " | " + str(self.pix)
        return hex(self.flags)

    def resolve(self):
        attributes = ""
        if (self.flags & 0x01) != 0:
            attributes += " public"
        if (self.flags & 0x02) != 0:
            attributes += " private"
        if (self.flags & 0x04) != 0:
            attributes += " protected"
        if (self.flags & 0x08) != 0:
            attributes += " static"
        if (self.flags & 0x10) != 0:
            attributes += " final"
        if (self.flags & 0x40) != 0:
            attributes += " abstract"
        if (self.flags & 0x80) != 0:
            attributes += " init"
        return attributes

class FieldAccessFlags(object):
    def __init__(self, flags):
        self.flags = ord(flags)

    def __repr__(self):
        return "< FieldAccessFlags Instance value:" + str(self.flags).encode('hex') + " >"

    def __str__(self):
        #return str(self.rid) + " | " + str(self.pix)
        return hex(self.flags)

    def resolve(self):
        attributes = ""
        if (self.flags & 0x01) != 0:
            attributes += " public"
        if (self.flags & 0x02) != 0:
            attributes += " private"
        if (self.flags & 0x04) != 0:
            attributes += " protected"
        if (self.flags & 0x08) != 0:
            attributes += " static"
        if (self.flags & 0x10) != 0:
            attributes += " final"
        return attributes

class ConstantPoolTag(object):
    def __init__(self, tag):
        self.tag = ord(tag)

    def __repr__(self):
        return "< ConstantPoolTag Instance value:" + str(self.tag).encode('hex') + " >"

    def __str__(self):
        #return str(self.rid) + " | " + str(self.pix)
        return str(self.tag)

    def resolve(self):
        attribute = ""
        if self.tag == 1:
            attribute = "Classref"
        elif self.tag == 2:
            attribute = "InstanceFieldref"
        elif self.tag == 3:
            attribute = "VirtualMethodref"
        elif self.tag == 4:
            attribute = "SuperMethodref"
        elif self.tag == 5:
            attribute = "StaticFieldref"
        elif self.tag == 6:
            attribute = "StaticMethodref"
        else:
            attribute = "Uknown tag"
        return attribute


class ClassBitField(object):
    def __init__(self, flags):
        self.flags = int(flags,16)

    def __repr__(self):
        return "< ClassBitField Instance value:" + str(self.flags).encode('hex') + " >"

    def __str__(self):
        #return str(self.rid) + " | " + str(self.pix)
        return hex(self.flags)

    def resolve(self):
        attributes = ""
        if (self.flags & 0x08) != 0:
            attributes += " interface"
        else:
            attributes += " class"
        if (self.flags & 0x04) != 0:
            attributes += " shareable"
        else:
            attributes += " non shareable"
        if (self.flags & 0x02) != 0:
            attributes += " remote"
        else:
            attributes += " non remote"     
        return attributes
