from scipy import stats



#transformer_filtered,fasttext_filtered



'''
transformer_restricted=[0.8308693171,0.8219988346,0.8081947565,0.8018923998,0.8040379882,0.8087885976,0.82007128,0.8052256703,0.813539207,0.7998812199,0.8277909756,0.801068902,0.8046318293,0.801068902,0.8248218298,0.807007134,0.8208160996,0.8034442067,0.807007134,0.8141329885]



#transformer_restricted=[0.8178592324,0.8160851598,0.8028503656,0.8231815696,0.8022565246,0.807600975,0.8111639023,0.8040379882,0.8052256703,0.8123515248,0.8206650615,0.8046318293,0.7969121337,0.8123515248,0.8129453659,0.8105700612,0.8249556422,0.7957244515,0.8058194518,0.8194774389]


fasttext_full = [0.8184506209,0.7924305145,0.8093824228,0.8060319338,0.8022565321,0.8081947743,0.8013010053,0.7975059382,0.7814726841,0.7874109264,0.804631829,0.7927553444,0.7980997625,0.7986935867,0.8159144893,0.7880047506,0.8040380048,0.7957244656,0.8070071259,0.7933491686]



stats.ttest_rel(transformer_restricted,fasttext_full)

stats.ttest_ind(transformer_restricted,fasttext_full)
'''

fasttext_filtered = [0.8260300850,0.8234139961,0.8161290323,0.8142576848,0.8248366013,0.8215686275,0.8090255069,0.8012903226,0.7916666667,0.7949709865,0.8096774194,0.8027343750,0.8046875000,0.8058823529,0.8206451613,0.7988281250,0.8110896196,0.8059316570,0.8098001289,0.8143790850]

lstm_filtered = [0.81098759174,0.81491172314,0.81483870745,0.79136693478,0.80980390310,0.79361981153,0.81237912178,0.80193549395,0.79361981153,0.82462924719,0.79161292315,0.79231768847,0.80273437500,0.79019606113,0.81548386812,0.80130720139,0.82668411732,0.80851066113,0.81431335211,0.81830066442]

atten_filtered = [0.8325703144,0.8273381591,0.8296774030,0.8312622905,0.8137254715,0.8111979365,0.8214055300,0.8187096715,0.8131510615,0.7981947064,0.8264515996,0.8111979365,0.8216145635,0.8215686083,0.8238709569,0.8209150434,0.8312622905,0.8065764308,0.8078659177,0.8169934750]

atten2_filtered = [0.827338159,0.824068010,0.823870957,0.830608249,0.820261419,0.806640625,0.824629247,0.821935475,0.819661438,0.805286884,0.824516118,0.805989563,0.813802063,0.816993475,0.829677403,0.821568608,0.829300225,0.805286884,0.814313352,0.815686285]


print('lstm_vs_fast: ', stats.ttest_rel(lstm_filtered,fasttext_filtered))
print('atten_vs_fast: ',stats.ttest_rel(atten_filtered,fasttext_filtered))
print('atten2_vs_fast: ',stats.ttest_rel(atten2_filtered,fasttext_filtered))
print('atten_vs_lstm: ',stats.ttest_rel(atten_filtered,lstm_filtered))
print('atten2_vs_lstm: ',stats.ttest_rel(atten2_filtered,lstm_filtered))
print('atten2_vs_atten: ',stats.ttest_rel(atten2_filtered,atten_filtered))


print('lstm_vs_fast: ', stats.ttest_ind(lstm_filtered,fasttext_filtered))
print('atten_vs_fast: ',stats.ttest_ind(atten_filtered,fasttext_filtered))
print('atten2_vs_fast: ',stats.ttest_ind(atten2_filtered,fasttext_filtered))
print('atten_vs_lstm: ',stats.ttest_ind(atten_filtered,lstm_filtered))
print('atten2_vs_lstm: ',stats.ttest_ind(atten2_filtered,lstm_filtered))
print('atten2_vs_atten: ',stats.ttest_ind(atten2_filtered,atten_filtered))

fasttext_res = [0.8184506209,0.7924305145,0.8093824228,0.8060319338,0.8022565321,0.8081947743,0.8013010053,0.7975059382,0.7814726841,0.7874109264,0.804631829,0.7927553444,0.7980997625,0.7986935867,0.8159144893,0.7880047506,0.8040380048,0.7957244656,0.8070071259,0.7933491686]

lstm_res = [0.8178592324,0.8054405451,0.8117577434,0.8013010025,0.7927553654,0.7915676832,0.8153206706,0.8058194518,0.7844418287,0.7891923785,0.8016626835,0.7891923785,0.7862232924,0.7951306701,0.7975059152,0.7992874384,0.8101714849,0.8058194518,0.807007134,0.8081947565]

atten_res = [0.8308693171,0.8219988346,0.8081947565,0.8018923998,0.8040379882,0.8087885976,0.82007128,0.8052256703,0.813539207,0.7998812199,0.8277909756,0.801068902,0.8046318293,0.801068902,0.8248218298,0.807007134,0.8208160996,0.8034442067,0.807007134,0.8141329885]

atten2_res = [0.8119456172,0.8267297745,0.8081947565,0.8214074373,0.8141329885,0.8016626835,0.8171021342,0.8105700612,0.8117577434,0.8123515248,0.813539207,0.7963182926,0.7933491468,0.8153206706,0.8260095119,0.8087885976,0.8184506297,0.7897862196,0.8123515248,0.8194774389]

print('lstm_vs_fast: ', stats.ttest_rel(lstm_res,fasttext_res))
print('atten_vs_fast: ',stats.ttest_rel(atten_res,fasttext_res))
print('atten2_vs_fast: ',stats.ttest_rel(atten2_res,fasttext_res))
print('atten_vs_lstm: ',stats.ttest_rel(atten_res,lstm_res))
print('atten2_vs_lstm: ',stats.ttest_rel(atten2_res,lstm_res))
print('atten2_vs_atten: ',stats.ttest_rel(atten2_res,atten_res))


print('lstm_vs_fast: ', stats.ttest_ind(lstm_res,fasttext_res))
print('atten_vs_fast: ',stats.ttest_ind(atten_res,fasttext_res))
print('atten2_vs_fast: ',stats.ttest_ind(atten2_res,fasttext_res))
print('atten_vs_lstm: ',stats.ttest_ind(atten_res,lstm_res))
print('atten2_vs_lstm: ',stats.ttest_ind(atten2_res,lstm_res))
print('atten2_vs_atten: ',stats.ttest_ind(atten2_res,atten_res))


print('fast: ', stats.ttest_rel(fasttext_filtered,fasttext_res))
print('LSTM: ',stats.ttest_rel(lstm_filtered,lstm_res))
print('atten: ',stats.ttest_rel(atten_filtered,atten_res))
print('atten2: ',stats.ttest_rel(atten2_filtered,atten2_res))


print('fast: ', stats.ttest_ind(fasttext_filtered,fasttext_res))
print('LSTM: ',stats.ttest_ind(lstm_filtered,lstm_res))
print('atten: ',stats.ttest_ind(atten_filtered,atten_res))
print('atten2: ',stats.ttest_ind(atten2_filtered,atten2_res))
