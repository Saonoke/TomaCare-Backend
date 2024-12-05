import enum

class penyakitEnum(enum.Enum):
    bacterial_spot = "Bacterial Spot"
    early_blight = "Early Blight"
    late_blight = "Late Blight"
    leaf_mold = "Leaf Mold"
    septorial_leaf_spot = "Septoria Leaf Spot"
    spidermites_two_spottedspider_mite = "Spidermites-Two-spottedspider_mite"
    target_spot = "Target Spot"
    tomato_yellow_leaf_curl_virus = "Tomato Yellow LeafCurl Virus"
    tomato_mosaic_virus = "Tomato mosaic virus"
    healthy = "Healthy"

    @staticmethod
    def get_enum_by_value(value:str):
        for penyakit in penyakitEnum:
            if penyakit.value == value:
                return penyakit
        return None
