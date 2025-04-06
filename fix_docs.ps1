# Fix ThinkAlike documentation

# Function to standardize filenames to lowercase
function Standardize-FileName {
    param()
    
     = [System.IO.Path]::GetDirectoryName()
     = [System.IO.Path]::GetFileNameWithoutExtension()
     = [System.IO.Path]::GetExtension()
    
    # Convert to lowercase with underscores
     = .ToLower() -replace '[ -]', '_'
     = Join-Path -Path  -ChildPath ""
    
    if ( -ne ) {
        Write-Host "Renaming:  -> " -ForegroundColor Yellow
        
        # Create the destination directory if it doesn't exist
         = [System.IO.Path]::GetDirectoryName()
        if (-not (Test-Path )) {
            New-Item -ItemType Directory -Path  -Force | Out-Null
        }
        
        # Try to rename the file
        try {
            Move-Item -Path  -Destination  -Force
        }
        catch {
            Write-Host "  Failed to rename, copying instead: " -ForegroundColor Red
            Copy-Item -Path  -Destination  -Force
        }
    }
    
    return 
}

# Find files that need to be renamed
 = @(
    "C:\--ThinkAlike--\docs\core\enlightenment_2_0\ENLIGHTENMENT_2_0_PRINCIPLES.md",
    "C:\--ThinkAlike--\docs\CONTRIBUTOR_FAQ.md"
)

foreach ( in ) {
    if (Test-Path ) {
         = Standardize-FileName -FilePath 
        
        # Update filepath references
         = Get-Content -Path  -Raw
         = [System.IO.Path]::GetDirectoryName()
         = [System.IO.Path]::GetFileNameWithoutExtension()
        
        # Replace uppercase filepath references with lowercase
         =  -replace "C:\\\\--ThinkAlike--\\\\docs\\\\core\\\\enlightenment_2_0\\\\ENLIGHTENMENT_2_0_PRINCIPLES\.md", "C:\\--ThinkAlike--\\docs\\core\\enlightenment_2_0\\enlightenment_2_0_principles.md"
         =  -replace "C:\\\\--ThinkAlike--\\\\docs\\\\CONTRIBUTOR_FAQ\.md", "C:\\--ThinkAlike--\\docs\\contributor_faq.md"
        
        Set-Content -Path  -Value 
        
        # Add to git
        git add 
    }
    else {
        Write-Host "File not found: " -ForegroundColor Red
    }
}

Write-Host "Documentation standardization complete!" -ForegroundColor Cyan
