import os

BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
all_expends: str = 'description,attrs,stocks,photos,photo_sizes,photo_3d_urls,video_file_url,grouped_attrs_list,barcodes,modifier_items,categories,all_categories,rating_stats,badges,seo,dataLayer,tags,ext_description,complete_set_description,wholesale_description,delivery_date,volume_discounts,materials,authors,notices,files,boxtype,extra_notices,small_modifiers,questions_count,special_offer_badge_label,special_offer,image_fragment_urls,has_analogs,cart_item,wish_item,is_delivery_to_door,retail_fee_markup,is_available_in_settlement,is_in_waiting_list'
first_keys = ["name", "short_name", "description", "ext_description", "stuff", 'depth', 'width', 'height', 'weight', 'size', 'volume', 'surface_area','country.name','trademark', 'series', 'series_id', 'min_age','power', 'has_light', 'has_sound', 'has_battery', 'is_inertial','complete_set_description', 'notices']
