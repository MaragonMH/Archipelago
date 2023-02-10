from ..dataType import Requirement as Req, Rule

def generate_friend_region(friend:str):
	return [ Rule("Menu"), *(Rule(f"{friend} {i}", [Req(f"FRD: {friend}", i)]) for i in range(1,6)) ]

friends_nagi_regions = generate_friend_region("Nagi")
friends_l_regions = generate_friend_region("L")
friends_lao_regions = generate_friend_region("Lao")
friends_gwin_regions = generate_friend_region("Gwin")
friends_frye_regions = generate_friend_region("Frye")
friends_doug_regions = generate_friend_region("Doug")
friends_phog_regions = generate_friend_region("Phog")
friends_elma_regions = generate_friend_region("Elma")
friends_lin_regions = generate_friend_region("Lin")
friends_celica_regions = generate_friend_region("Celica")
friends_irina_regions = generate_friend_region("Irina")
friends_murderess_regions = generate_friend_region("Murderess")
friends_hope_regions = generate_friend_region("Hope")
friends_mia_regions = generate_friend_region("Mia")
