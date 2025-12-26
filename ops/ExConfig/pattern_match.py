import bpy
from ...utils.config_manager import ConfigManager
from ...utils.path_analyzer import PathAnalyzer


# ------------------------------------------------------------------------
# ExConfig Pattern Match - Operator
# ------------------------------------------------------------------------
class EXCONFIG_OT_GeneratePatternMatch(bpy.types.Operator):
    bl_idname = "exconfig.generate_pattern_match"
    bl_label = "Generate Pattern Match"
    bl_description = "Generate variable mapping between two patterns"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        exconfig = context.scene.exconfig
        
        # Validate inputs
        if exconfig.project_list == 'NONE':
            self.report({'ERROR'}, "No project selected")
            return {'CANCELLED'}
        
        if exconfig.pattern_match_source == 'NONE':
            self.report({'ERROR'}, "No source pattern selected")
            return {'CANCELLED'}
        
        if exconfig.pattern_match_target == 'NONE':
            self.report({'ERROR'}, "No target pattern selected")
            return {'CANCELLED'}
        
        if exconfig.pattern_match_source == exconfig.pattern_match_target:
            self.report({'ERROR'}, "Source and target patterns must be different")
            return {'CANCELLED'}
        
        project_name = exconfig.project_list
        source_pattern_name = exconfig.pattern_match_source
        target_pattern_name = exconfig.pattern_match_target
        
        # Get patterns
        source_pattern = ConfigManager.get_pattern_from_config(project_name, source_pattern_name)
        target_pattern = ConfigManager.get_pattern_from_config(project_name, target_pattern_name)
        
        if not source_pattern:
            self.report({'ERROR'}, f"Source pattern '{source_pattern_name}' not found")
            return {'CANCELLED'}
        
        if not target_pattern:
            self.report({'ERROR'}, f"Target pattern '{target_pattern_name}' not found")
            return {'CANCELLED'}
        
        # Get variable names and example values
        source_vars = source_pattern.get("variable_names", [])
        target_vars = target_pattern.get("variable_names", [])
        source_examples = source_pattern.get("example_values", {})
        target_examples = target_pattern.get("example_values", {})
        
        print("=" * 60)
        print("DEBUG: Pattern Match Generation")
        print("=" * 60)
        print(f"Source pattern '{source_pattern_name}':")
        print(f"  Variable names: {source_vars}")
        print(f"  Example values: {source_examples}")
        print(f"\nTarget pattern '{target_pattern_name}':")
        print(f"  Variable names: {target_vars}")
        print(f"  Example values: {target_examples}")
        print("=" * 60)
        
        if not source_vars:
            self.report({'ERROR'}, f"No variables in source pattern")
            return {'CANCELLED'}
        
        if not target_vars:
            self.report({'ERROR'}, f"No variables in target pattern")
            return {'CANCELLED'}
        
        # Match by example values (case-insensitive)
        # If target example value matches source example value, map to that source variable NAME
        # Otherwise, save the target example value as a string literal
        mapping = {}
        
        print("\nMatching process:")
        print("-" * 60)
        
        for target_var in target_vars:
            target_value = target_examples.get(target_var, "")
            matched = False
            
            print(f"\nProcessing target variable: {target_var} = '{target_value}'")
            
            # Try to find a source variable with matching example value
            for source_var in source_vars:
                source_value = source_examples.get(source_var, "")
                
                print(f"  Checking source: {source_var} = '{source_value}'")
                
                # Case-insensitive comparison
                if target_value.lower() == source_value.lower():
                    mapping[target_var] = source_var  # Save variable NAME
                    matched = True
                    print(f"  ✓ MATCH! Saving: {target_var} -> {source_var} (variable name)")
                    break
            
            # If no match found, save the target example value as a string
            if not matched:
                mapping[target_var] = target_value  # Save static VALUE
                print(f"  ✗ No match. Saving: {target_var} -> '{target_value}' (static value)")
        
        print("=" * 60)
        print(f"Final mapping: {mapping}")
        print("=" * 60)
        
        # Create match name
        match_name = f"{source_pattern_name.lower()}_{target_pattern_name.lower()}"
        
        # Save to config
        success = ConfigManager.save_pattern_match(project_name, match_name, mapping)
        
        if success:
            self.report({'INFO'}, f"Pattern match saved: {match_name}")
            print(f"Pattern match '{match_name}': {mapping}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to save pattern match")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(EXCONFIG_OT_GeneratePatternMatch)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_OT_GeneratePatternMatch)
