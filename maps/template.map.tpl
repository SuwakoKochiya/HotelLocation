MAP
	NAME "MyMap"
	STATUS ON
	
	EXTENT 427628.956897 4396182.996554 473167.587649 4433548.026914
	IMAGETYPE AGG_PNG
	MAXSIZE 2048
	RESOLUTION 72
	
	SYMBOL
		NAME "Circle"
		FILLED true
		TYPE ellipse
		POINTS 1 1 END
    END
	
	DEBUG OFF
	
	PROJECTION
		"ellps=WGS84" "a=6378137"
		"rf=298.257223563" "datum=WGS84"
		"units=m" "proj=tmerc"
		"x_0=500000.0" "y_0=0.0"
		"lon_0=117.0" "k_0=0.9996"
		"lat_0=0.0"
	END
	
	LEGEND
		IMAGECOLOR 0 0 0
		POSITION lr
		STATUS on
		KEYSIZE 20 10
		KEYSPACING 5 5
		POSTLABELCACHE FALSE
		LABEL
			PRIORITY 1
			MAXSIZE 256
			MINSIZE 4
			##BACKGROUNDSHADOWSIZE 1 1
			ANTIALIAS FALSE
			FORCE FALSE
			PARTIALS TRUE
		END
	END
	
	SCALEBAR
		COLOR 128 128 128
		BACKGROUNDCOLOR 0 0 0
		IMAGECOLOR 255 255 255
		OUTLINECOLOR 192 192 192
		ALIGN center
		STATUS on
		UNITS meters
		SIZE 300 5
		INTERVALS 4
		INTERLACE FALSE
		POSTLABELCACHE FALSE
	END
	
	WEB
		METADATA
			"wms_title" "Beijing_Hotel"
			"wms_onlineresource" "http://vps2.fdugis.info/cgi-bin/mapserv.exe?map=$mappath&"
			"wms_srs" "EPSG:32650"
			"wms_enable_request" "*"
		END
	END
	
	OUTPUTFORMAT
		NAME "AGG_PNG"
		DRIVER "AGG/PNG"
		IMAGEMODE RGBA
		EXTENSION png
		TRANSPARENT ON
	END
	
	LAYER		
		NAME "Road_region_shp"
		TYPE polygon
		STATUS ON
		OPACITY 100
		SIZEUNITS pixels
		DATA "/var/www/maps/road_region_shp"
		DUMP FALSE
		OFFSITE 0 0 0
		METADATA
			"ows_title" "Road_region_shp"
			"wms_title" "Road_region_shp"
		END
		LABELCACHE on
		POSTLABELCACHE FALSE
		TRANSFORM true
		CLASS
			NAME "Untitled class"
			STYLE
				ANTIALIAS TRUE
				WIDTH 0.35 
				OUTLINECOLOR 0 0 0
				COLOR 135 144 30
			END
		END
	END
	
	LAYER
		NAME 'restaurant_point_shp'
		TYPE POINT
		DATA '/var/www/maps/restaurant_point_shp.shp'
		METADATA
			'ows_title' 'restaurant_point_shp'
		    'wms_title' 'restaurant_point_shp'
        END
		STATUS ON
		TRANSPARENCY 100
		CLASS
			NAME 'restaurant_point_shp' 
			STYLE
				SYMBOL "circle" 
				SIZE 7.0
				OUTLINECOLOR 0 0 0
				COLOR 214 14 141
			END
		END
	END
	
	LAYER
		NAME 'subwaystation_font_point_shp'
		TYPE POINT
		DATA '/var/www/maps/subwaystation_font_point_shp.shp'
		METADATA
			'ows_title' 'subwaystation_font_point_shp'
            'wms_title' 'subwaystation_font_point_shp'
		END
		STATUS ON
		TRANSPARENCY 100
		CLASS
			NAME 'subwaystation_font_point_shp' 
			STYLE
				SYMBOL "circle" 
				SIZE 10.5 
				OUTLINECOLOR 0 0 0
				COLOR 67 64 241
			END
		END
	END
	
	LAYER
		
		NAME "grid_final_in4"
		TYPE polygon
		STATUS OFF
		OPACITY 100
		SIZEUNITS pixels
		DATA "$layerpath"
		CLASSITEM "mymymy"
		DUMP FALSE
		OFFSITE 0 0 0
		METADATA
			"ows_title" "grid_final_in4"
			"wms_title" "grid_final_in4"
		END
		PROJECTION
			"ellps=WGS84" "a=6378137"
			"rf=298.257223563" "datum=WGS84"
			"units=m" "proj=tmerc"
			"x_0=500000.0" "y_0=0.0"
			"lon_0=117.0" "k_0=0.9996"
			"lat_0=0.0"
		END
		LABELCACHE on
		POSTLABELCACHE FALSE
		TRANSFORM true
		CLASS
			NAME "0.0 - 0.2"
			STATUS on
			EXPRESSION ([mymymy]<0.2)
			STYLE
				ANTIALIAS FALSE
				SYMBOL 0
				SIZE 1
				ANGLE 0
				OPACITY 100
				COLOR 245 245 0
				OUTLINECOLOR 128 128 128
				WIDTH 1
			END
		END
		CLASS
			NAME "0.2 - 0.4"
			EXPRESSION (([mymymy]>=0.2)  And ([mymymy] < 0.4))
			STYLE
				ANTIALIAS FALSE
				SYMBOL 0
				SIZE 1
				ANGLE 0
				OPACITY 100
				COLOR 245 184 0
				OUTLINECOLOR 128 128 128
				WIDTH 1
			END
		END
		CLASS
			NAME "0.4 - 0.6"
			EXPRESSION (([mymymy]>=0.4)  And ([mymymy] < 0.6))
			STYLE
				ANTIALIAS FALSE
				SYMBOL 0
				SIZE 1
				ANGLE 0
				OPACITY 100
				COLOR 245 122 0
				OUTLINECOLOR 128 128 128
				WIDTH 1
			END
		END
		CLASS
			NAME "0.6 - 0.8"
			EXPRESSION (([mymymy]>=0.6)  And ([mymymy] < 0.8))
			STYLE
				ANTIALIAS FALSE
				SYMBOL 0
				SIZE 1
				ANGLE 0
				OPACITY 100
				COLOR 245 61 0
				OUTLINECOLOR 128 128 128
				WIDTH 1
			END
		END
		CLASS
			NAME "0.8 - 1.0"
			EXPRESSION ([mymymy]>=0.8)
			STYLE
				ANTIALIAS FALSE
				SYMBOL 0
				SIZE 1
				ANGLE 0
				OPACITY 100
				COLOR 161 0 0
				OUTLINECOLOR 128 128 128
				WIDTH 1
			END
		END
	END
	  
	LAYER
		NAME 'hotelproj'
		TYPE POINT
		DUMP true
		DATA '/var/www/maps/hotelproj.shp'
		METADATA
			'ows_title' 'hotelproj'
		END
		STATUS ON
		TRANSPARENCY 49
		CLASS
		   NAME 'hotelproj'
		   STYLE
			 SYMBOL "circle"
			 SIZE 7.0
			 OUTLINECOLOR 0 0 0
			 COLOR 0 85 0
		   END
		END
	END
	
	
END
