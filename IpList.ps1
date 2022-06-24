Write-Host "Authenticating to Azure..." -ForegroundColor Cyan
try
{
    $AzureLogin = Get-AzureRmSubscription
}
catch
{
    $null = Login-AzureRmAccount
    $AzureLogin = Get-AzureRmSubscription
}

$FileName = ""
$downloadUri = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'
$downloadPage = Invoke-WebRequest -Uri $downloadUri
$jsonFileUri = ($downloadPage.RawContent.Split('"') -like "https://*ServiceTags*")[0]
if( $FileName -eq "" ) {
	$NameParts = $jsonFileUri.Split('/')
	if ( -Not (Test-Path "$PSScriptRoot\downloads") ) {
		New-Item -Path "$PSScriptRoot\downloads" -ItemType directory
	}
	$FileName = "$PSScriptRoot\downloads\$($NameParts[ $NameParts.Count - 1 ])"
} 
(New-Object System.Net.WebClient).DownloadFile($jsonFileUri, "C:\downloads\ServiceTags_Public_20180723.json")
$FileName


Get-Content $FileName |
ConvertFrom-Json  |
Select -Expand values | 
Select @{Name="Name"; Expression={ $_.name}}, 
	@{Name="Region"; Expression={ $_.properties.Region}},
	@{Name="Ranges"; Expression={ $_.properties.addressPrefixes.count}},
	@{Name="Version"; Expression={ $_.properties.changeNumber}}	| 
Sort-Object Name