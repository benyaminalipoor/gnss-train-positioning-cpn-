#!/usr/bin/env python3
"""
CPN File Validator and Test Runner
Validates the GNSS_Train_Positioning.cpn file structure
"""

import xml.etree.ElementTree as ET
import sys

def validate_cpn_file(filename):
    """Validate CPN file structure and content"""
    print(f"Validating {filename}...")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    try:
        # Parse XML
        tree = ET.parse(filename)
        root = tree.getroot()
        print("✓ XML is well-formed")
        
        # Check root element
        if root.tag != "workspaceElements":
            errors.append(f"Root element should be 'workspaceElements', got '{root.tag}'")
        else:
            print("✓ Root element is correct")
        
        # Check for generator
        generator = root.find('.//generator')
        if generator is not None:
            tool = generator.get('tool')
            version = generator.get('version')
            fmt = generator.get('format')
            print(f"✓ Generator: {tool} {version}, format {fmt}")
        else:
            warnings.append("No generator information found")
        
        # Check for cpnet element
        cpnet = root.find('.//cpnet')
        if cpnet is None:
            errors.append("No cpnet element found")
            return errors, warnings
        
        print("✓ Found cpnet element")
        
        # Check global declarations
        globbox = cpnet.find('.//globbox')
        if globbox is None:
            errors.append("No globbox (global declarations) found")
        else:
            ml = globbox.find('.//ml')
            if ml is None:
                errors.append("No ML code in globbox")
            else:
                ml_text = ml.text or ""
                ml_lines = ml_text.strip().split('\n')
                print(f"✓ Global declarations: {len(ml_lines)} lines of ML code")
                
                # Check for essential components
                if "colset" not in ml_text:
                    errors.append("No color sets defined")
                else:
                    colset_count = ml_text.count("colset")
                    print(f"  - Color sets: {colset_count}")
                
                if "fun " not in ml_text:
                    warnings.append("No functions defined")
                else:
                    fun_count = ml_text.count("fun ")
                    print(f"  - Functions: {fun_count}")
                
                if "var " not in ml_text:
                    errors.append("No variables defined")
                else:
                    var_count = ml_text.count("var ")
                    print(f"  - Variables: {var_count}")
                
                # Check for essential functions
                essential_funcs = [
                    'generateSignals',
                    'ekfPredict',
                    'ekfUpdate',
                    'calculateError',
                    'calculateRMSE',
                    'generateTestScenario'
                ]
                
                for func in essential_funcs:
                    if func not in ml_text:
                        errors.append(f"Essential function '{func}' not found")
                    else:
                        print(f"  ✓ Found function: {func}")
        
        # Check pages
        pages = cpnet.findall('.//page')
        if not pages:
            errors.append("No pages found")
        else:
            print(f"\n✓ Found {len(pages)} page(s):")
            
            expected_pages = [
                "Top Level",
                "GNSS Receiver",
                "Position Solution",
                "Evaluation"
            ]
            
            found_pages = []
            for page in pages:
                page_attr = page.find('.//pageattr')
                if page_attr is not None:
                    page_name = page_attr.get('name', 'Unnamed')
                    found_pages.append(page_name)
                    
                    places = page.findall('.//place')
                    trans = page.findall('.//trans')
                    arcs = page.findall('.//arc')
                    
                    print(f"  - '{page_name}': {len(places)} places, {len(trans)} transitions, {len(arcs)} arcs")
                    
                    if len(places) == 0:
                        warnings.append(f"Page '{page_name}' has no places")
                    if len(trans) == 0:
                        warnings.append(f"Page '{page_name}' has no transitions")
            
            # Check for expected pages
            for expected in expected_pages:
                if expected not in found_pages:
                    warnings.append(f"Expected page '{expected}' not found")
        
        # Check monitors
        monitors = cpnet.findall('.//monitor')
        if monitors:
            print(f"\n✓ Found {len(monitors)} monitor(s):")
            for monitor in monitors:
                name = monitor.find('.//name')
                if name is not None:
                    print(f"  - {name.text}")
        else:
            warnings.append("No monitors found (simulation may run indefinitely)")
        
        # Check options
        options = cpnet.find('.//options')
        if options is not None:
            option_list = options.findall('.//option')
            print(f"\n✓ Found {len(option_list)} simulation option(s)")
        
        # Summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        
        if errors:
            print(f"\n❌ {len(errors)} ERROR(S) FOUND:")
            for i, err in enumerate(errors, 1):
                print(f"  {i}. {err}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} WARNING(S):")
            for i, warn in enumerate(warnings, 1):
                print(f"  {i}. {warn}")
        
        if not errors and not warnings:
            print("\n✓ ✓ ✓ CPN file is VALID and COMPLETE! ✓ ✓ ✓")
            return True
        elif not errors:
            print("\n✓ CPN file is VALID (with warnings)")
            return True
        else:
            print("\n❌ CPN file has ERRORS that must be fixed")
            return False
        
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_scenario_info():
    """Print information about available scenarios"""
    print("\n" + "=" * 60)
    print("AVAILABLE SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        (1, "OpenArea", "Normal", "Best conditions"),
        (2, "OpenArea", "AM", "AM interference"),
        (3, "OpenArea", "FM", "FM interference (worst in open)"),
        (4, "OpenArea", "Pulse", "Pulse interference"),
        (5, "Mountain", "Normal", "Mountain terrain"),
        (6, "Mountain", "AM", "Mountain + AM"),
        (7, "Mountain", "FM", "Mountain + FM"),
        (8, "Mountain", "Pulse", "Mountain + Pulse"),
        (9, "Tunnel", "Normal", "Tunnel/urban canyon"),
        (10, "Tunnel", "AM", "Tunnel + AM"),
        (11, "Tunnel", "FM", "Tunnel + FM (worst overall)"),
        (12, "Tunnel", "Pulse", "Tunnel + Pulse"),
    ]
    
    print("\nID | Environment | Interference | Description")
    print("-" * 60)
    for sid, env, interf, desc in scenarios:
        print(f"{sid:2d} | {env:10s} | {interf:12s} | {desc}")
    
    print("\nExpected RMSE Trends:")
    print("  Interference: Normal < AM < Pulse < FM")
    print("  Environment:  OpenArea < Mountain < Tunnel")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "GNSS_Train_Positioning.cpn"
    
    result = validate_cpn_file(filename)
    print_scenario_info()
    
    sys.exit(0 if result else 1)
