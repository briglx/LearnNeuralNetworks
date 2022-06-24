####### Search Service Tags  ############
Get-Content $FileName |
ConvertFrom-Json  |
Select -Expand values | 
Select @{Name="Name"; Expression={ $_.name}}, 
	@{Name="Region"; Expression={ $_.properties.Region}},
	@{Name="Ranges"; Expression={ $_.properties.addressPrefixes.count}},
	@{Name="Version"; Expression={ $_.properties.changeNumber}}	| 
where { ($_.Name -like $Name) -and ( $_.Region -like $Region) } |
Sort-Object Name