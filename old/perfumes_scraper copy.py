import json
from perfumes_db_helper import PerfumesDBHelper
from urllib import request, error
from selenium import webdriver
from bs4 import BeautifulSoup
from seleniumwire import webdriver
import time
from lxml import html
from lxml import etree
import csv


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main():
    DB = PerfumesDBHelper("perfumes.sqlite")
    DB.setup()

    # Use selenium instead of requests
    # requests isnt working
    # get 403 from fragrantica
    browser = webdriver.Firefox()

    with open("perfumes_manifest.txt", "r") as f:
        perfume_urls = f.readlines()
    number_of_perfumes = len(perfume_urls)

    with open("data.csv", "w") as csv_file:
        wr = csv.writer(csv_file)

        header = ["brand", "perfume","rating", "votes" "accord1", "accord2", "accord3", "l_weak", "l_mmoderate", "l_longlast", "l_verylonglast", "s_weak", 
                 "s_moderate", "s_huge", "s_enormous", "rating", "votes", "winter", "autumn", "spring", "summer"]
        wr.writerow(header)

    # flag = DB.number_of_records()
        flag = 0
        for index in range(flag, number_of_perfumes):
            # try:
                url = perfume_urls[index][:-1]

                row = []
                # Use selenium to get URL
                browser.get(url)
                soup = BeautifulSoup(browser.page_source, 'lxml') # error
                tree = etree.HTML(str(soup))
                brand_and_perfume = url[35:-6].split("/")
                brand = brand_and_perfume[0].replace("-", " ")
                perfume_title = brand_and_perfume[1].split("-")
                perfume_title = " ".join(perfume_title[:-1])

                row.append(brand)        


                # perfume_image_url = tree.xpath("//meta[@property='og:image']/@content")[0]
                # if perfume_image_url:
                #     perfume_image_file_name = perfume_image_url.split("/")[-1]
                #     request.urlretrieve(perfume_image_url, "fragrantica_images/perfumes/" + perfume_image_file_name)
                # else:
                #     perfume_image_file_name = None
                # perfume = {"title": perfume_title, "image": perfume_image_file_name}
                perfume = perfume_title # perfume is only the title, no image
                row.append(perfume)

                # page_title = tree.xpath("//title/text()")[0]
                # if not page_title:
                #     launch_year = None
                # else:
                #     launch_year = page_title[-4:]
                #     if not represents_int(launch_year):
                #         launch_year = None

                ###################### Get rating ####################
                ratings = tree.xpath("/html/body/div[4]/div[3]/div/div/div[1]/div/div/div/div/div[6]/p/span[1]/text()")
                if ratings:
                    rating = float(ratings[0])
                else:
                    # r
                    continue
                    # contineating = continue
                row.append(rating)

                ###################### Get votes ####################
                voting = tree.xpath("/html/body/div[3]/div[3]/div/div/div[1]/div/div/div/div/div[6]/p/span[3]/text()")

                if voting:
                    votes = int(voting[0])
                else:
                    continue
                row.append(votes)

                ###################### Get accords ####################
                main_accords = tree.xpath("//div[@id='prettyPhotoGallery']/div/div/span/text()")
                if main_accords:
                    if "main accords" in main_accords:
                        main_accords.remove("main accords")
                    if "Videos" in main_accords:
                        main_accords.remove("Videos")
                    if "Pictures" in main_accords:
                        main_accords.remove("Pictures")
                else:
                    # main_accords = continue
                    continue
                # set 2 main accords
                # multiply accord by pixel width
                if main_accords is not None:                        
                    row.append(main_accords[0])
                    row.append(main_accords[1])
                    row.append(main_accords[3])
                else:
                    continue
                    # row.append(None)
                    # row.append(None)
                    # row.append(None)

                ###################### Get notes ####################
                # notes_captions = tree.xpath("//h3/text()")
                # notes = {}
                # if "Fragrance Notes" in notes_captions:
                #     note_tags = tree.xpath("//span[@class='rtgNote']/img")
                #     notes["general"] = [note_tag.get("title") for note_tag in note_tags]
                # elif "Perfume Pyramid" in notes_captions:
                #     top_notes = tree.xpath("//p[b/text()='Top Notes']/span[@class='rtgNote']/img")
                #     middle_notes = tree.xpath("//p[b/text()='Middle Notes']/span[@class='rtgNote']/img")
                #     base_notes = tree.xpath("//p[b/text()='Base Notes']/span[@class='rtgNote']/img")
                #     if top_notes:
                #         notes["top"] = [top_note.get("title") for top_note in top_notes]
                #     else:
                #         notes["top"] = None
                #     if middle_notes:
                #         notes["middle"] = [middle_note.get("title") for middle_note in middle_notes]
                #     else:
                #         notes["middle"] = None
                #     if base_notes:
                #         notes["base"] = [base_note.get("title") for base_note in base_notes]
                #     else:
                #         notes["base"] = None
                # else:
                #     notes = None


                ############### Get Longevity ###############
                longevity_votes = tree.xpath("//table[@class='voteLS long']/tr/td[@class='ndSum']/text()")
                print(longevity_votes)
                if longevity_votes:
                    longevity_ints = [int(i) for i in longevity_votes]
                    # longevity = {"poor": int(longevity_votes[0]), "weak": int(longevity_votes[1]), "moderate": int(longevity_votes[2]),
                    #             "long lasting": int(longevity_votes[3]), "very long lasting": int(longevity_votes[4])}
                    # longevity = [int(longevity_votes[0]), int(longevity_votes[1]), 
                    #             int(longevity_votes[2]),int(longevity_votes[3]), int(longevity_votes[4])]
                    s = sum(longevity_ints)
                    # print(s)
                    norm_longevity = [(float(i)/ s) for i in longevity_ints]

                    for n in norm_longevity:
                        row.append(n)
                else:
                    continue
                    # norm_longevity = None
                    # for i in range(5):
                    #     row.append(None)

                # print(row)

                ###################### Get sillage ####################
                sillage_votes = tree.xpath("/html/body/div[3]/div[3]/div/div/div[1]/div/div/div/div/div[8]/div[2]/table/tbody/tr/td/table/tbody/tr/td[@class='ndSum']/text()")
                print(sillage_votes)
                if sillage_votes:
                    # sillage = {"soft": sillage_votes[0], "moderate": sillage_votes[1], "heavy": sillage_votes[2],
                    #         "enormous": sillage_votes[3]}
                    sillage_ints = [int(i) for i in sillage_votes]
                    s = sum(sillage_ints)
                    norm_sillage = [(float(i) / s) for i in sillage_ints]

                    for n in norm_sillage:
                        row.append(n)
                else:
                    continue
                    # norm_sillage = None
                    # for i in range(5):
                    #     row.append(None)



                ###################### Get season ####################
                winter = tree.xpath("//*[@id='clswinterD']")
                win_v = winter[0].values()[1].split()[3]
                win_v = win_v[:-3]

                autumn = tree.xpath("//*[@id='clsautumnD']")
                au_v = autumn[0].values()[1].split()[3]# [1].split()[3]
                au_v = au_v[:-3]

                spring = tree.xpath("//*[@id='clsspringD']")
                sp_v = spring[0].values()[1].split()[3]
                sp_v = sp_v[:-3]

                summer = tree.xpath("//*[@id='clssummerD']")
                su_v = summer[0].values()[1].split()[3]# [1].split()[3]
                su_v = su_v[:-3]

                row.append(int(win_v))
                row.append(int(au_v))
                row.append(int(sp_v))
                row.append(int(su_v))
                # Print progress    
                print({"count": "{0}/{1}".format(index, number_of_perfumes), "brand": brand, "perfume": perfume})

                # DB.add_record(tuple([brand, perfume, launch_year, json.dumps(main_accords), json.dumps(notes),
                #                     json.dumps(longevity), json.dumps(sillage)]))

                # wr.writerow(row)
                print(row)
                break

            # except:
            #     continue

if __name__ == "__main__":
    main()
