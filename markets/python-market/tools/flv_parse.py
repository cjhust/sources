import struct
import sys
import os


def usage(progname):
    print('usage: %s <file_path>' % progname)
    sys.exit(0)


def parse_flv_header(file):
    print("---------parse flv header---------")
    box_format = {
        "signature": 3,
        "version": 1,
        "flags": 1,
        "dataoffset": 4,
        "previous_tagsize": 4
    }
    
    # > 表示大端
    #signature: 3字节，"FLV"
    data = file.read(box_format["signature"])
    signature = str(struct.unpack(">3s", data)[0])
    print("signature: ", signature)
    
    #version: 1字节
    data = file.read(box_format["version"])
    version = struct.unpack("B", data)[0]
    print("version: ", version) 
    
    #flags: 1字节，一般是0x5=101，表示存在音频和视频
    data = file.read(box_format["flags"])
    flags = struct.unpack("B", data)[0]
    print("flags: ",flags)
    
    #dataoffset: 4字节
    data = file.read(box_format["dataoffset"])
    dataoffset = struct.unpack(">I", data)[0]
    print("data_offset: ",dataoffset) 
    
    #previous_tagsize: 4字节, 第1个tagsize=0
    data = file.read(box_format["previous_tagsize"])
    previous_tagsize = struct.unpack(">I", data)[0]
    print("previous_tagsize: ", previous_tagsize)
    
    return 13


    
def parse_flv_script_array_type(data, offset, array_size):
    end_flag = 0
    while array_size:
        #key length: 2字节
        keylength = struct.unpack(">I", b'\x00' + b'\x00' + data[offset:offset+2])[0]
        offset += 2
        
        key = str(data[offset:offset+keylength], encoding='utf-8')
        offset += keylength
        
        #data_type: 1字节
        datatype = struct.unpack(">B", data[offset:offset+1])[0]
        offset += 1
        print("    [script array tag]: length:", keylength, ", key:", key, ", type:", datatype) 
        
        #number: type（1字节）+ 数据(8字节)
        if datatype == 0:
            offset += 8 
        
        #boolean: type（1字节）+ 数据(1字节)  
        elif datatype == 1:
            offset += 1 
        
        #string: type（1字节）+长度（2字节）+data
        elif datatype == 2: 
            data_size = struct.unpack(">I", b'\x00' + b'\x00' + data[offset:offset+2])[0]
            offset += 2
            offset += data_size  
            
        #date: type（1字节）+长度（10字节)   
        elif datatype == 11: 
            offset += 10    
        
        #object: type（1字节）+长度（10字节)   
        elif datatype == 3: 
            end_flag += 1 
               
        #object_end: type（1字节）+长度（10字节)   
        elif datatype == 9: 
            if end_flag == 0:
                break     
            end_flag -= 1     
        
        #strict_array: type（1字节）+长度（10字节) 
        #times and filepositions  
        elif datatype == 10: 
            object_size = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4 
           
            while object_size > 0:
                object_size -= 1
                #data_type: 1字节
                datatype = struct.unpack(">B", data[offset:offset+1])[0]
                offset += 1
    
                #number类型（double）
                if datatype == 0:
                    offset += 8 
                else:
                    print("    [script array tag]: must double type in array type")
                    sys.exit(-3)         
        else:
            print("    [script array tag]: unkown data type")
            sys.exit(-2)
    pass


#first AMF packet
#type（1字节, string）+长度（2字节, 值为10）+"onMetaData"

#second AMF packet
#type（1字节, array）+长度（2字节, 值为10）+"onMetaData"

#onMetaData
def parse_flv_script_tag(data, tagsize):  
    offset = 0
    end_flag = 0
    while offset < tagsize:
        #data_type: 1字节
        datatype = struct.unpack(">B", data[offset:offset+1])[0]
        offset += 1 
        print("  [script tag]: data type: ", datatype)
        
        #number: type（1字节）+ 数据(8字节)
        if datatype == 0:
            offset += 8 
        
        #boolean: type（1字节）+ 数据(1字节)  
        elif datatype == 1:
            offset += 1 
        
        #string: type（1字节）+长度（2字节）+data
        elif datatype == 2: 
            data_size = struct.unpack(">I", b'\x00' + b'\x00' + data[offset:offset+2])[0]
            offset += 2          
            offset += data_size
        
        #object: type（1字节）+长度（10字节)   
        elif datatype == 3: 
            offset += 10 
        
        #array: type（1字节）+长度（10字节)   
        elif datatype == 8:
            array_size = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            print("  [script tag]: array size: ", array_size)           
            parse_flv_script_array_type(data, offset, array_size)
        
        #date: type（1字节）+长度（10字节)   
        elif datatype == 11: 
            offset += 10    
        
        #object: type（1字节）+长度（10字节)   
        elif datatype == 3: 
            end_flag += 1 
               
        #object_end: type（1字节）+长度（10字节)   
        elif datatype == 9: 
            if end_flag == 0:
                break     
            end_flag -= 1 
        else:
            print("  [script tag]: unkown data type")
            sys.exit(-2)


def parse_flv_tag(file):
    print("\n---------parse flv tag---------")
    box_format = {
        "tag_type": 1,
        "tag_data_size": 3,
        "timestamp": 3,
        "timestamp_extended":1,
        "stream_id": 3,
        "previous_tagsize": 4
    }  
    
    #tag_type: 1字节
    data = file.read(box_format["tag_type"])
    tag_type = struct.unpack(">B", data)[0]
    if tag_type == 18:
        print("tag type: script")
    elif tag_type == 9:
        print("tag type: video")
    elif tag_type == 8:
        print("tag type: audio")
    else:
        print("bad tag")
        sys.exit(-2)
    
    #tag_data_size: 3字节
    data = b'\x00' + file.read(box_format["tag_data_size"]) 
    tag_data_size = struct.unpack(">I", data)[0]
    print("tag_data_size: ", tag_data_size)
    
    #timestamp + timestamp_extended + stream_id: 3+1+3=7字节
    data = file.read(box_format["timestamp"] + box_format["timestamp_extended"] + box_format["stream_id"])
    data = file.read(int(tag_data_size))
    if tag_type == 18: 
        parse_flv_script_tag(data, tag_data_size)
    
    #previous_tagsize: 4字节
    data = file.read(box_format["previous_tagsize"])
    previous_tagsize = struct.unpack(">I", data)[0]
    print("previous_tagsize: ", previous_tagsize)
    
    if previous_tagsize != 11 + tag_data_size :
        print("tag size not equal")
        sys.exit(-2)
    
    return previous_tagsize + 4
        
 
def parse_flv_file(filename):
    file = open(filename, "rb")
    
    file_size = os.path.getsize(filename)
    file_size -= parse_flv_header(file) 
    
    count = 0  
    while file_size > 0:
        #解析3个tag就退出
        count += 1
        if count > 3:
            break        

        read_size = parse_flv_tag(file)
        file_size -= read_size
    #while end
    file.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage(sys.argv[0])

    filename = sys.argv[1]
    parse_flv_file(filename)
