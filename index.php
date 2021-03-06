<?php session_start(); ?>
<html lang="zh-Hant-TW">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<?php
		if($_SESSION['email'] != null)
			echo "<title>" . $_SESSION['email'] . "</title>";
		else
			echo "<title>大河小溪全民齊督工</title>";			
		?>
		<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico">
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" />
		<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" />
		<link rel="stylesheet" href="src/leaflet.fusesearch.css" />
		<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"></script>
		<script src="src/fuse.js"></script>
		<script src="src/leaflet.fusesearch.js"></script>
		<link href="http://fonts.googleapis.com/earlyaccess/notosanstc.css" rel="stylesheet" type="text/css">
		<style>  <!--視窗大小控制-->
		<!--
			@media (min-width: 0px) {
				#nm-screen{
					display: none;
					background-color: red;					
				}
				#sm-screen{
					display: flex;
				}
			}-->
			@media (min-width: 576px) {
				#sm-screen{
					display: none;
				}
				#nm-screen{
					display: flex;
					background-color: yellow;
				}
			}
			@media (min-width: 768px) {
				#sm-screen{
					display: none;
				}
				#nm-screen{
					display: flex;
					background-color: orange;
				}
			}
		</style>
		<style> <!--map style-->
		</style>
		<style> <!--other style-->
			html, body {
				height: 100%;
			}
			a, h1, h2 {
				font-family: 'noto sans tc';
				text-decoration: none;
			}
			#sm-screen, #nm-screen {
				height: 100vh;
			}
			#map {				
				display: block;
				height: 100%;
			}
		</style>
	</head>
	<body><!--
			<div id="sm-screen" style="border-radius: 20px;">
				<div class="d-flex flex-column"><h2>手機螢幕尺寸</h2></div>
			</div>-->
			<div id="nm-screen" class="d-flex flex-column">
				<nav class="navbar navbar-light bg-light navbar-expand-sm ">
					<a class="navbar-brand" href="#">大河小溪全民齊督工</a>
					<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
						<span class="navbar-toggler-icon"></span>
					</button>
					<div class="collapse navbar-collapse" id="navbarNav">					
					<ul class="navbar-nav">
						<li class="nav-item active">
							<a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
						</li>
						<li class="nav-item">
							<a class="nav-link" target="_blank" href="http://bambooculture.com/about">關於我們</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" target="_blank" href="https://beta.hackfoldr.org/bcsrcsp">相關連結</a>
						</li>
					</ul>
					</div>
				</nav>
				
				<div id="map" class="container-fluid"></div>
			</div>
			<script src="src/osm_river.geojson"></script>
			<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
			<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
			<script>
				var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://www.mapbox.com/">mapbox</a> ',
					mbUrl = 'https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoianMwMDE5MyIsImEiOiJjandjYWtwem0wYnB3NDlvN2h0anRuM3Z1In0.Y7tYEgVHjszA66NQ08PVYg'
					osmUrl= 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
				var satellite = L.tileLayer(mbUrl, {id: 'satellite-v9',   attribution: mbAttr}),
					satellite_street = L.tileLayer(mbUrl, {id: 'satellite-streets-v11',   attribution: mbAttr}),
					streets  = L.tileLayer(osmUrl, {attribution: mbAttr});
				

				function onEachFeature(features, layer) {
					features.layer = layer;
					var name, wikiid, osmid;
					if(features['properties']['@relations'] && features['properties']['@relations']['reltags']){
						name = features['properties']['@relations']['reltags']['name'];
						wikiid = features['properties']['@relations']['reltags']['wikidata'];
						osmid = "rel/" + features['properties']['@relations']['rel'];						
					}
					else{
						name = features.properties.name;
						wikiid = features.properties.wikidata;
						osmid = features.id;
					}
					layer.bindPopup('<button class="btn btn-info" id="'+osmid+'">訂閱'+name+'</button><p>wikidata: ' + wikiid + "<br>id: " + osmid+"</p>");
				}
				
				var river_info_layer = L.geoJSON(river_geojson, {
					pointToLayer: function (feature, latlng) {
					},					
					onEachFeature: onEachFeature,
					style: {
						"weight": 50,
						"opacity": 0.01,
					}
				});
				var river_layer = L.geoJSON(river_geojson, {
					pointToLayer: function (feature, latlng) {
					},					
					style: {
						"weight": 3,
						"opacity": 0.75,
						"bubblingMouseEvents": false
					}
				});
				/*
				var NorthWest = L.latLng(32.876668, 115.669328),
					SouthEast = L.latLng(32.833433, 115.738169);
				var bounds = L.latLngBounds(SouthEast, NorthWest);	*/
				
				var mymap = L.map('map', {
					center: [25.1426293,121.4592866],
					zoom: 18,
					maxZoom: 18,
					minZoom: 7,
					layers: [satellite, streets],
					zoomControl:true
				});		
				
				var baseMaps = {
					"空照圖": satellite,
					//"空照街道": satellite_street,
					
					"街道圖": streets,
				};
				/*
				var overlayMaps = {			
					"河川河道": river_layer,
				};								*/
				var searchCtrl = L.control.fuseSearch()
				searchCtrl.addTo(mymap);
				searchCtrl.indexFeatures(river_geojson, ['name', '@id','wikidata']);
				river_info_layer.addTo(mymap);
				river_layer.addTo(mymap);
				L.control.layers(baseMaps, null).addTo(mymap);				
				
				$('#map').on('click', '#btn1', function() {
					alert('BCS!!');
				});
			</script>
			</script>
	</body>
</html>
