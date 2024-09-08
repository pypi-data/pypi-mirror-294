# from . import logger
from . import get_logger
from custom_development_standardisation import *
from flask import Flask, jsonify, request,  make_response, send_file



import base64



# class deconstructuing_message():
#     def __init__(self):
class constructing_message():
    
    def __init__(self):
        self.response = make_response()
        # self.response.headers["outcome"] = False
        self.response.headers['Access-Control-Expose-Headers'] = 'boundaries'
        self.bounary = None
        self.Content_type = None 
        self.parts = []
    
    def set_multipart_message_config(self,boundary_string=None):
        if boundary_string == None or isinstance(boundary_string,str) == False:
            return generate_outcome_message("error","bounary_string parameter cannot be empty and cannot be not of type string...",the_type="custom")

        self.bounary = boundary_string
        self.Content_type = 'multipart/mixed'
        return generate_outcome_message("success","Set message content and boundary string...")

    # def message_checker(self,Content_type,Content_Disposition):
    
    def construct_image_section(self,name,image_path=None,image_binary=None):
        try:
            get_logger().store_log()
        except Exception as e:
            None

        if image_binary == None and image_path == None:
            return generate_outcome_message("error","No image to process...",the_type="custom")
        base64_data = None
        if image_binary == None:
            try:
                with open(image_path,'rb') as img:
                    current_image = img.read()
                    base64_data = base64.b64encode(current_image)
            except:
                return generate_outcome_message("error",f"something is wrong with image path {image_path}...",the_type="custom")
            
        if image_path == None:
            if isinstance(image_binary, (bytes, bytearray)) == False:
                return generate_outcome_message("error","image_binary parameter is not of in binary format...",the_type="custom")
            base64_data = base64.b64encode(image_binary)    
        
        utf_8 = base64_data.decode('utf-8')
        put_together = (
            'number-system:base64\r\n'
            f'name:{name}\r\n'
            'data-type:image/jpeg\r\n'
            f'data:{utf_8}\r\n'
        )
        self.parts.append(put_together)

        return generate_outcome_message("success","image section appended...")
    
    def construct_text_section(self,name,text):
        try:
            get_logger.store_log()
        except Exception as e:
            None

        if isinstance(text,str) == False:
            return generate_outcome_message("error","text parameter is not a string...",the_type="custom")
        put_together = (
            f'name:{name}\r\n'
            'data-type:text\r\n'
            f'data:{text}\r\n'
        )
        self.parts.append(put_together)
        return generate_outcome_message("success","image section appended...")
        
    def construct_encoded_multipart_message(self):
        
        self.response.mimetype = 'multipart/form-data'
        self.response.headers['Content-Type'] = f'multipart/form-data'
        self.response.headers['boundaries'] = f'{self.bounary}'
        final = ""
        for i in self.parts:
            final += f"--{self.bounary}--\r\n"
            final += i
        # print(final)
        encoded = final.encode('utf-8')
        self.response.data = encoded
        return self.response



# x = constructing_message()
# x.set_multipart_message_config('lala')
# x.construct_image_section("car.jpeg",image_path="/Users/marcus/Desktop/AI/projects/render_back_end_behaviour_check/car.jpeg")
# x.construct_text_section("something","nothing")
# x.construct_encoded_multipart_message()


