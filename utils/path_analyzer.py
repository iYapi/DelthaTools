import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class PathPattern:
    """Data class to hold path pattern information"""

    name: str
    base_path: str
    folder_patterns: List[str]
    filename_pattern: str
    file_extension: str
    variable_names: List[str]
    example_values: Dict[str, str]
    example_path: str


class PathAnalyzer:
    """Manages path patterns - detection and reconstruction"""

    def __init__(self, json_file: Optional[str] = None, data: Optional[Dict] = None):
        self.json_file = json_file
        self.patterns: Dict[str, PathPattern] = {}
        
        # Load from dict if provided
        if data:
            self.load_from_dict(data)
        # Otherwise load from file if it exists
        elif json_file and os.path.exists(json_file):
            self.load_patterns()

    def load_from_dict(self, data: Dict) -> None:
        """Load patterns from dictionary data"""
        patterns_data = data.get("patterns", {})
        if not patterns_data:
            return

        for name, pattern_data in patterns_data.items():
            try:
                # Remove full_pattern if it exists (it's a computed field, not stored in dataclass)
                pattern_data_copy = pattern_data.copy()
                pattern_data_copy.pop('full_pattern', None)
                pattern = PathPattern(**pattern_data_copy)
                self.patterns[name] = pattern
            except Exception as e:
                print(f"Warning: Could not load pattern '{name}': {e}")

    def detect_pattern(self, full_path: str, base_path: str) -> tuple:
        """
        Detect complete pattern structure from a full path
        Returns: (folder_patterns, filename_pattern, file_extension, variable_map, variable_names)
        """
        # Normalize paths
        base_path = os.path.normpath(base_path)
        full_path = os.path.normpath(full_path)

        # Verify full path starts with base path
        if not full_path.startswith(base_path):
            raise ValueError(
                f"Path must start with base path.\nBase: {base_path}\nFull: {full_path}"
            )

        # Remove base path
        relative_path = full_path[len(base_path):].lstrip(os.path.sep)

        # Split into components
        parts = relative_path.split(os.path.sep) if relative_path else []

        if not parts:
            raise ValueError("No path components after base path")

        # Get filename and folders
        filename = parts[-1]
        folders = parts[:-1]

        # Extract filename parts
        file_base, file_ext = os.path.splitext(filename)

        # Track all values and assign variables
        value_to_var = {}
        var_to_value = {}
        next_var_index = 0

        def get_variable_for_value(value: str) -> str:
            nonlocal next_var_index

            if value in value_to_var:
                return value_to_var[value]
            else:
                var_name = f"var_{next_var_index}"
                value_to_var[value] = var_name
                var_to_value[var_name] = value
                next_var_index += 1
                return var_name

        # Process folders
        folder_patterns = []
        for folder in folders:
            if "_" in folder:
                folder_parts = folder.split("_")
                pattern_parts = []
                for part in folder_parts:
                    var_name = get_variable_for_value(part)
                    pattern_parts.append(f"{{{var_name}}}")
                folder_pattern = "_".join(pattern_parts)
            else:
                var_name = get_variable_for_value(folder)
                folder_pattern = f"{{{var_name}}}"
            folder_patterns.append(folder_pattern)

        # Process filename
        file_parts = file_base.split("_")
        filename_pattern_parts = []
        for part in file_parts:
            var_name = get_variable_for_value(part)
            filename_pattern_parts.append(f"{{{var_name}}}")

        filename_pattern = "_".join(filename_pattern_parts)
        variable_names = [f"var_{i}" for i in range(next_var_index)]

        return folder_patterns, filename_pattern, file_ext, var_to_value, variable_names

    def create_pattern(
        self, name: str, base_path: str, full_path: str, save_example: bool = True
    ) -> PathPattern:
        """Create a pattern from a path"""
        folder_patterns, filename_pattern, file_ext, var_values, var_names = (
            self.detect_pattern(full_path, base_path)
        )

        pattern = PathPattern(
            name=name,
            base_path=base_path,
            folder_patterns=folder_patterns,
            filename_pattern=filename_pattern,
            file_extension=file_ext,
            variable_names=var_names,
            example_values=var_values if save_example else {},
            example_path=full_path if save_example else "",
        )

        return pattern

    def save_pattern(self, pattern: PathPattern, output_file: Optional[str] = None) -> None:
        """Save a pattern to JSON file"""
        if output_file:
            self.json_file = output_file

        if not self.json_file:
            raise ValueError("No output file specified")

        # Add pattern to collection
        self.patterns[pattern.name] = pattern

        # Save to file
        self._save_to_json()

    def _save_to_json(self) -> None:
        """Save all patterns to JSON file"""
        if not self.json_file:
            raise ValueError("No JSON file path specified")

        data = {"patterns": {}}

        for name, pattern in self.patterns.items():
            pattern_dict = asdict(pattern)
            # Add full_pattern to the exported data
            pattern_dict["full_pattern"] = self.get_full_pattern_string(name)
            data["patterns"][name] = pattern_dict

        try:
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(os.path.abspath(self.json_file))
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"Patterns saved to: {os.path.abspath(self.json_file)}")

        except Exception as e:
            print(f"Error saving to {self.json_file}: {e}")
            raise

    def get_pattern(self, pattern_name: str) -> Optional[PathPattern]:
        """Get a pattern by name"""
        return self.patterns.get(pattern_name)

    def build_path(self, pattern_name: str, variables: Optional[Dict[str, str]] = None, match: Optional[str] = None, pattern_matches: Optional[Dict[str, Dict[str, str]]] = None) -> str:
        """
        Build a path from pattern using provided variables
        
        Args:
            pattern_name: Name of the pattern to build
            variables: Variable values to use
            match: Optional match name (e.g., "animation_playblast") to remap variables
            pattern_matches: Optional pattern match dictionary (e.g., {"animation_playblast": {"var_0": "var_1"}})
        
        Returns:
            Built path string
            
        Example:
            # Without matching
            build_path("Playblast", {"var_0": "03", "var_1": "010"})
            
            # With matching (remaps animation vars to playblast vars)
            build_path("Playblast", {"var_1": "03", "var_2": "010"}, 
                       match="animation_playblast",
                       pattern_matches={"animation_playblast": {"var_0": "var_1", "var_1": "var_2"}})
        """
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        # If match is specified, remap variables
        if match and pattern_matches and match in pattern_matches:
            mapping = pattern_matches[match]
            remapped_vars = {}
            
            # Remap: left side is target pattern var, right side is either:
            #   - A source pattern variable name (e.g., "var_1")
            #   - A static string value (e.g., "playblast")
            # E.g., {"var_0": "var_1"} means playblast.var_0 = animation.var_1
            # E.g., {"var_6": "playblast"} means playblast.var_6 = "playblast" (static)
            if variables:
                for target_var, source_var in mapping.items():
                    if source_var in variables:
                        # It's a source variable name, use its value
                        remapped_vars[target_var] = variables[source_var]
                        print(f"Mapping {target_var} from source variable {source_var}: {variables[source_var]}")
                    else:
                        # It's a static string value, use it directly
                        remapped_vars[target_var] = source_var
                        print(f"Using static value for {target_var}: '{source_var}'")
                
                variables = remapped_vars
        
        if variables is None:
            variables = pattern.example_values

        if not variables:
            raise ValueError(
                f"No variables provided and no example values saved for pattern '{pattern_name}'"
            )

        missing_vars = [var for var in pattern.variable_names if var not in variables]
        if missing_vars:
            raise ValueError(f"Missing variables: {', '.join(missing_vars)}")

        path_parts = [pattern.base_path]

        for folder_pattern in pattern.folder_patterns:
            folder_name = folder_pattern
            for var_name, var_value in variables.items():
                placeholder = f"{{{var_name}}}"
                if placeholder in folder_name:
                    folder_name = folder_name.replace(placeholder, var_value)
            path_parts.append(folder_name)

        filename = pattern.filename_pattern
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            if placeholder in filename:
                filename = filename.replace(placeholder, var_value)

        full_filename = filename + pattern.file_extension
        path_parts.append(full_filename)

        return os.path.join(*path_parts)

    def analyze_path(self, base_path: str, full_path: str) -> Dict:
        """
        Analyze a path and return complete pattern information
        """
        folder_patterns, filename_pattern, file_ext, var_values, var_names = (
            self.detect_pattern(full_path, base_path)
        )

        full_pattern_parts = [base_path]
        full_pattern_parts.extend(folder_patterns)
        full_pattern_parts.append(filename_pattern + file_ext)
        full_pattern = os.path.join(*full_pattern_parts)

        return {
            "base_path": base_path,
            "folder_patterns": folder_patterns,
            "filename_pattern": filename_pattern + file_ext,
            "full_pattern": full_pattern,
            "variables": var_names,
            "example_values": var_values,
            "example_path": full_path,
            "total_variables": len(var_names),
        }

    def get_full_pattern_string(self, pattern_name: str) -> str:
        """Get the complete pattern as a single string"""
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            return ""

        parts = [pattern.base_path]
        parts.extend(pattern.folder_patterns)
        parts.append(pattern.filename_pattern + pattern.file_extension)
        return os.path.join(*parts)

    def load_patterns(self, json_file: Optional[str] = None) -> None:
        """Load patterns from JSON file"""
        if json_file:
            self.json_file = json_file

        if not self.json_file or not os.path.exists(self.json_file):
            return

        try:
            with open(self.json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.load_from_dict(data)
            print(f"Loaded {len(self.patterns)} pattern(s) from {self.json_file}")

        except json.JSONDecodeError as e:
            print(f"Error: Pattern file {self.json_file} is not valid JSON: {e}")
        except Exception as e:
            print(f"Error loading patterns from {self.json_file}: {e}")

    def list_patterns(self) -> List[str]:
        """List all available pattern names"""
        return list(self.patterns.keys())

    def delete_pattern(self, pattern_name: str) -> bool:
        """Delete a pattern by name"""
        if pattern_name in self.patterns:
            del self.patterns[pattern_name]
            if self.json_file:
                self._save_to_json()
            return True
        return False

    def to_dict(self) -> Dict:
        """Export all patterns to dictionary"""
        data = {"patterns": {}}
        
        for name, pattern in self.patterns.items():
            pattern_dict = asdict(pattern)
            # Add full_pattern to the exported data
            pattern_dict["full_pattern"] = self.get_full_pattern_string(name)
            data["patterns"][name] = pattern_dict
        
        return data

    def extract_variables(self, pattern_name: str, file_path: str) -> Optional[Dict[str, str]]:
        """
        Extract variable values from a file path using a pattern
        
        Args:
            pattern_name: Name of the pattern to use
            file_path: Full file path to extract variables from
            
        Returns:
            Dictionary of variable names to values, or None if path doesn't match pattern
            
        Example:
            pattern: "/base/{var_0}/{var_1}_{var_2}/{var_3}.blend"
            path: "/base/animation/ep102_sq01/sh0100.blend"
            returns: {"var_0": "animation", "var_1": "ep102", "var_2": "sq01", "var_3": "sh0100"}
        """
        import re
        
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            raise ValueError(f"Pattern '{pattern_name}' not found")
        
        # Normalize the file path
        file_path = os.path.normpath(file_path)
        
        # Build the full pattern string
        pattern_parts = [pattern.base_path]
        pattern_parts.extend(pattern.folder_patterns)
        pattern_parts.append(pattern.filename_pattern + pattern.file_extension)
        full_pattern = os.path.join(*pattern_parts)
        
        # Normalize the pattern path
        full_pattern = os.path.normpath(full_pattern)
        
        # Convert pattern to regex
        # Escape special regex characters except our placeholders
        regex_pattern = re.escape(full_pattern)
        
        # Track which variables we've already seen and their capture group indices
        var_group_map = {}  # {var_name: [group_index1, group_index2, ...]}
        group_counter = 1
        
        # Replace escaped placeholders with capture groups
        # Use named groups for first occurrence, non-capturing groups for duplicates
        for var_name in pattern.variable_names:
            escaped_placeholder = re.escape(f"{{{var_name}}}")
            
            # Count occurrences of this variable in the pattern
            count = regex_pattern.count(escaped_placeholder)
            
            if count == 0:
                continue
            
            if var_name not in var_group_map:
                # First occurrence: use named group
                regex_pattern = regex_pattern.replace(
                    escaped_placeholder,
                    f"(?P<{var_name}>[^{re.escape(os.sep)}]+)",
                    1  # Replace only first occurrence
                )
                var_group_map[var_name] = [group_counter]
                group_counter += 1
                
                # Replace remaining occurrences with backreferences
                for i in range(count - 1):
                    regex_pattern = regex_pattern.replace(
                        escaped_placeholder,
                        f"(?P={var_name})",  # Backreference to first occurrence
                        1
                    )
        
        # Try to match the path
        regex_pattern = f"^{regex_pattern}$"
        match = re.match(regex_pattern, file_path)
        
        if not match:
            return None
        
        # Extract all variables
        variables = match.groupdict()
        return variables

    def extract_variables_from_dict(self, pattern_dict: Dict, file_path: str) -> Optional[Dict[str, str]]:
        """
        Extract variable values from a file path using a pattern dictionary
        (doesn't require pattern to be loaded into PathAnalyzer)
        
        Args:
            pattern_dict: Pattern dictionary (from get_pattern_dict())
            file_path: Full file path to extract variables from
            
        Returns:
            Dictionary of variable names to values, or None if path doesn't match pattern
            
        Example:
            pattern_dict = exconfig.get_pattern_dict()
            variables = analyzer.extract_variables_from_dict(pattern_dict, current_file_path)
        """
        import re
        
        # Normalize the file path
        file_path = os.path.normpath(file_path)
        
        # Build the full pattern string
        base_path = pattern_dict.get("base_path", "")
        folder_patterns = pattern_dict.get("folder_patterns", [])
        filename_pattern = pattern_dict.get("filename_pattern", "")
        file_extension = pattern_dict.get("file_extension", "")
        variable_names = pattern_dict.get("variable_names", [])
        
        pattern_parts = [base_path]
        pattern_parts.extend(folder_patterns)
        pattern_parts.append(filename_pattern + file_extension)
        full_pattern = os.path.join(*pattern_parts)
        
        # Normalize the pattern path
        full_pattern = os.path.normpath(full_pattern)
        
        # Convert pattern to regex
        regex_pattern = re.escape(full_pattern)
        
        # Replace escaped placeholders with capture groups
        for var_name in variable_names:
            escaped_placeholder = re.escape(f"{{{var_name}}}")
            regex_pattern = regex_pattern.replace(
                escaped_placeholder, 
                f"(?P<{var_name}>[^{re.escape(os.sep)}]+)"
            )
        
        # Try to match the path
        regex_pattern = f"^{regex_pattern}$"
        match = re.match(regex_pattern, file_path)
        
        if not match:
            return None
        
        # Extract all variables
        variables = match.groupdict()
        return variables
