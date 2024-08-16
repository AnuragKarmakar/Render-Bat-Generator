bl_info = {
    "name": "Render Batch generator",
    "description": "Generates the batch to start the rendering without using the GUI\nThere's no Documentation page for this addon for now!",
    "author": "AnuragKarmakar",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "location": "Render > Generate Batch File",
    "warning": "Windows-only Script, I do not encourage usage on other Operating Systems.", # used for warning icon and text in addons panel
    "doc_url": "https://docs.blender.org/manual/en/latest/advanced/command_line/render.html",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Render",
}
import bpy

def batch_render_menu(self, scene) :
    layout = self.layout
    layout.separator()
    layout.operator("render.generate_batch_file", text="Generate render batch file")

class BTH_OT_GenerateBatchFile(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "render.generate_batch_file"
    bl_label = "Render : Generate batch file"
    
    def execute(self, context):
        
        if(bpy.data.is_dirty):
            self.report({'INFO'}, "Please save the .blend file")
            return {'FINISHED'}
        else:
        
            #Project informations

            scn = context.scene
            render = scn.render            
            engine = context.scene.render.engine
            samples = scn.eevee.taa_render_samples
            if engine == "CYCLES" :
                samples = scn.cycles.samples
            frame_start = scn.frame_start
            frame_end = scn.frame_end
            res_x = render.resolution_x
            res_y = render.resolution_y
            res_percent = render.resolution_percentage
            fps = render.fps
            filepath = render.filepath
            file_format = render.image_settings.file_format
            color_mode = render.image_settings.color_mode
            
            ffmpeg_data = ""
            if file_format == "FFMPEG" :
                ffmpeg_data = " - " + render.ffmpeg.codec + " / " + render.ffmpeg.audio_codec
            
            
            #Generate project information to warn the user
            information = [    "Renders information :",
                                "Render engine : " + engine + " with " + str(samples) + " samples",
                                "Render path : " + filepath,
                                "Type of render : Animation",
                                "FPS : " + str(fps),
                                "File format : " + file_format + " (" + color_mode + ")" + ffmpeg_data,
                                "Resolution : " + str(int(res_x*res_percent/100)) + " by " + str(int(res_y*res_percent/100)) + 
                                    " (" + str(res_percent) + " percent of " + str(res_x) + " by " + str(res_y) + ")",
                                "Frame range : Start:" + str(frame_start) + " to End:" + str(frame_end)
                            ]

             
    
            #Cmmmand line parameters these aren't necessary to be honest
            b_path = bpy.app.binary_path
            bg_command = "-b"
            project_path = bpy.data.filepath
            render_option = "-a"                #Hard coded animation feature will add more here on future releases
            
                        
            project_name = bpy.path.basename(bpy.data.filepath).split(".")[0]
                        
            #Generate the batch file 
            file = open(bpy.path.abspath("//") + "renderbatch_" + project_name + ".bat", "w")
            
            #Write the project status on the batch
            file.write("@echo off\n")
            file.write("color e\n")
            for info in information :
                file.write("echo " + info + "\n")
            
            notifications = ["echo ========",
                                "echo Please check the informations then press any key to start the renders",
                                "echo If a parameter is wrong, do not press any key and close the console",
                                "pause",
                                "echo Thank you for using my Script!",
                                "color 2",
                                "echo Rendering Now!",
                                "color",]
            
            for n in notifications :
                file.write(n + "\n")
            
                
            #Write the project command line that start the rendering
            file.write('\"' + b_path + '\" ' + bg_command + ' "' + project_path + '" ' + render_option + "\n")
            
            #Close the file
            file.close()
            
            self.report({'INFO'}, "Batch file generated!")

            
            return {'FINISHED'}


classes = [BTH_OT_GenerateBatchFile]

def register():
    
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_render.append(batch_render_menu)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_render.remove(batch_render_menu)


if __name__ == "__main__":
    register()
