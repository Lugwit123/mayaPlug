import unreal
 
import_path =r"G:\BLDTD\Shot\PV02\sc01\shot014\UE\pre_production_data\Animation\PV02_sc01_shot014_C_ChenXiang_anitolgt.fbx"
 
import_extension = unreal.Paths.get_extension(import_path, False)
 
is_gltf = import_extension == 'glb' or import_extension == 'gltf'
is_fbx = import_extension == 'fbx'
is_usd = import_extension == 'usd'
 
#if you want to import fbx file make sure interchange fbx import is enabled
if is_fbx:
    level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    unreal.SystemLibrary.execute_console_command(level_editor_subsystem.get_world(), 'Interchange.FeatureFlags.Import.FBX true')
 
    
#if you want to import fbx file make sure interchange fbx import is enabled
if is_usd:
    level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    unreal.SystemLibrary.execute_console_command(level_editor_subsystem.get_world(), 'Interchange.FeatureFlags.Import.USD true')
 
editor_asset_subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
 
transient_path = "/Interchange/Pipelines/Transient/"
transient_pipeline_path = transient_path + "MyAutomationPipeline"
 
editor_asset_subsystem.delete_directory(transient_path)
 
#Duplicate the default interchange asset content pipeline, gltf have a special assets
if is_gltf:
    pipeline = editor_asset_subsystem.duplicate_asset("/Interchange/Pipelines/DefaultGLTFAssetsPipeline", transient_pipeline_path)
elif is_usd:
    pipeline = editor_asset_subsystem.duplicate_asset("/InterchangeOpenUSD/Pipelines/DefaultUSDAssetsPipeline", transient_pipeline_path)
else:
    pipeline = editor_asset_subsystem.duplicate_asset("/Interchange/Pipelines/DefaultAssetsPipeline", transient_pipeline_path)
 
#Set any pipelines properties you need for your asset import here
 
#force static mesh import
# pipeline.common_meshes_properties.force_all_mesh_as_type = unreal.InterchangeForceMeshType.IFMT_STATIC_MESH
# pipeline.common_meshes_properties.force_all_mesh_as_type = unreal.InterchangeForceMeshType.IFMT_STATIC_MESH
pipeline.common_skeletal_meshes_and_animations_properties.import_only_animations = False
#combine static mesh
pipeline.mesh_pipeline.combine_static_meshes = True
if not is_usd:
    #Prevent Material import
    pipeline.material_pipeline.import_materials = False
    #Prevent Texture import
    pipeline.material_pipeline.texture_pipeline.import_textures = False
 
#Create a source data from the filename 
source_data = unreal.InterchangeManager.create_source_data(import_path)
#create the parameters for the interchange import
import_asset_parameters = unreal.ImportAssetParameters()
#Script is normaly an automated import
import_asset_parameters.is_automated = True
 
#Add the configured pipeline to the import arguments
import_asset_parameters.override_pipelines.append(unreal.SoftObjectPath(transient_pipeline_path + ".MyAutomationPipeline"))
#gltf importer use 2 pipeline add the second one
if is_gltf:
    import_asset_parameters.override_pipelines.append(unreal.SoftObjectPath("/Interchange/Pipelines/DefaultGLTFPipeline"))
elif is_usd:
    import_asset_parameters.override_pipelines.append(unreal.SoftObjectPath("/InterchangeOpenUSD/Pipelines/DefaultUSDPipelineAssetImport"))
    import_asset_parameters.override_pipelines.append(unreal.SoftObjectPath("/Interchange/Pipelines/DefaultMaterialXPipeline"))
 
interchange_manager = unreal.InterchangeManager.get_interchange_manager_scripted()
 
#Edit translator settings in case of USD to set materialX import
cached_translator = interchange_manager.get_translator_for_source_data(source_data)
cached_translator_settings = cached_translator.get_settings()
 
translator = interchange_manager.get_translator_for_source_data(source_data)
translator_settings = translator.get_settings()
if is_usd:
    translator_settings.set_editor_property("render_context", "mtlx")
    #necessary for settings to apply on import, but will change for all imports
    translator_settings.save_settings()
 
#import the asset
interchange_manager.import_asset("/game/AA0A/testpython/",source_data,import_asset_parameters)
 
#reset translator settings: done by resaving the original settings into config file
cached_translator_settings.save_settings()
 
#clean temporary folder to remove temporary pipelines
editor_asset_subsystem.delete_directory(transient_path)