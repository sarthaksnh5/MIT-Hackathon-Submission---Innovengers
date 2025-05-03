def process_business_card(ocr_text: List[str]) -> None:
    """
    Process a business card OCR text array using LLM and search for matching LinkedIn profiles.
    
    Implements a tiered search strategy:
    1. Try full name + company in keywords
    2. If no results, try full name + job title in keywords
    3. If still no results, try just full name in keywords
    
    Args:
        ocr_text: List of strings from OCR processing
    """
    print("Processing business card OCR text...")
    
    # Process the business card using the LLM processor
    processor = LLMBusinessCardProcessor(ocr_text)
    card_info = processor.extract_information()
    
    print("\nExtracted Information from LLM:")
    print(json.dumps(card_info, indent=2))
    
    # Initialize the LinkedIn profile finder
    finder = LinkedInProfileFinder()
    
    # Check if we have the required fields for search
    has_name = bool(card_info['full_name'])
    has_company = bool(card_info['company'])
    has_job_title = bool(card_info['job_title'])
    
    if not has_name:
        print("\nERROR: No name found in the business card. Cannot perform LinkedIn search.")
        return
    
    # TIER 1: Search with full name + company in keywords
    if has_name and has_company:
        print("\n=== TIER 1 SEARCH: Full Name + Company ===")
        search_params = {
            'keywords': f"{card_info['full_name']} {card_info['company']}",
            'start': '0',
            'max': '10'
        }
        
        print(f"Searching with parameters:")
        print(json.dumps(search_params, indent=2))
        
        profiles = finder.search_profiles(search_params)
        
        # If we found results, return them
        if profiles:
            print("\nFound results with TIER 1 search (name + company).")
            display_profiles(profiles)
            return
    
    # TIER 2: Search with full name + job title in keywords
    if has_name and has_job_title:
        print("\n=== TIER 2 SEARCH: Full Name + Job Title ===")
        search_params = {
            'keywords': f"{card_info['full_name']} {card_info['job_title']}",
            'start': '0',
            'max': '10'
        }
        
        print(f"Searching with parameters:")
        print(json.dumps(search_params, indent=2))
        
        profiles = finder.search_profiles(search_params)
        
        # If we found results, return them
        if profiles:
            print("\nFound results with TIER 2 search (name + job title).")
            display_profiles(profiles)
            return
    
    # TIER 3: Search with just full name
    print("\n=== TIER 3 SEARCH: Full Name Only ===")
    search_params = {
        'keywords': card_info['full_name'],
        'start': '0',
        'max': '10'
    }
    
    print(f"Searching with parameters:")
    print(json.dumps(search_params, indent=2))
    
    profiles = finder.search_profiles(search_params)
    
    if profiles:
        print("\nFound results with TIER 3 search (name only).")
        display_profiles(profiles)
    else:
        print("\nNo matching LinkedIn profiles found after all search attempts.")


def display_profiles(profiles: List[Dict[str, Any]]) -> None:
    """
    Display the LinkedIn profiles in a formatted way.
    
    Args:
        profiles: List of LinkedIn profile dictionaries
    """
    print("\nMatching LinkedIn Profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"\nProfile {i}:")
        print(f"Name: {profile['name']}")
        print(f"Headline: {profile['headline']}")
        
        if 'location' in profile and profile['location']:
            print(f"Location: {profile['location']}")
        
        if 'position' in profile and profile['position']:
            print(f"Current Position: {profile['position']}")
        
        if 'company' in profile and profile['company']:
            print(f"Current Company: {profile['company']}")
        
        if 'profile_url' in profile and profile['profile_url']:
            print(f"Profile URL: {profile['profile_url']}")
        
        # Display experience if available
        if 'experience' in profile and profile['experience']:
            print("\nExperience:")
            for exp in profile['experience']:
                print(f"  - {exp['title']} at {exp['company']} ({exp['duration']})")
        
        # Display education if available
        if 'education' in profile and profile['education']:
            print("\nEducation:")
            for edu in profile['education']:
                print(f"  - {edu['degree']} in {edu['field']} at {edu['school']}")
        
        # Display raw response if available (for debugging)
        if 'raw_response' in profile:
            print(f"\nAPI Response: {profile['raw_response']}")