# LDA topic model recommender

topic_num = 50, user_items > 20

## neighbors = 50, recommend_item = 20
- average precision : 0.0726611226611
- average recall : 0.055617364826
- average f1 : 0.0513593822837

## neighbors = 50, recommend_item = 30
- average precision : 0.0686763686764
- average recall : 0.0783148141215
- average f1 : 0.0595898713843

## neighbors = 50, recommend_item = 50
- average precision : 0.0609563409563
- average recall : 0.112909214625
- average f1 : 0.0649452142284

# Tag based user-similar recommender

topic_num = 50, user_items > 20

## neighbors = 50, recommend_item = 20
- average precision : 0.0904365904366
- average recall : 0.0762809320236
- average f1 : 0.0669150533426

## neighbors = 50, recommend_item = 30
- average precision : 0.0864171864172
- average recall : 0.108225022876
- average f1 : 0.0778033044046

## neighbors = 50, recommend_item = 50
- average precision : 0.0779625779626
- average recall : 0.160449822302
- average f1 : 0.0859543965989

# user_item based recommender

topic_num = 50, user_items > 20

## neighbors = 50, recommend_item = 10
- average precision : 0.0972972972973
- average recall : 0.0443521350818
- average f1 : 0.051458344037

## neighbors = 50, recommend_item = 20
- average precision : 0.0951143451143
- average recall : 0.0825060303165
- average f1 : 0.0719504853011

## neighbors = 50, recommend_item = 30
average precision : 0.0907137907138
average recall : 0.115046576291
average f1 : 0.0828386431591

## neighbors = 50, recommend_item = 50
average precision : 0.0814553014553
average recall : 0.166177003394
average f1 : 0.0903493993086


# LDA topic model and tag-based hybrid recommender

topic_num = 50, user_items > 20

## neighbors = 10, recommend_item = 20
- average precision : 0.081288981289
- average recall : 0.0673944275774
- average f1 : 0.0602131668176


## neighbors = 50, recommend_item = 20
<!-- - average precision : 0.0844074844075
- average recall : 0.0715017946214
- average f1 : 0.0628156030996 -->
- average precision : 0.0855509355509
- average recall : 0.0726793437386
- average f1 : 0.0641195565713


## neighbors = 50, recommend_item = 30
- average precision : 0.080595980596
- average recall : 0.0994021239206
- average f1 : 0.0719489714399


## neighbors = 50, recommend_item = 50
- average precision : 0.0722661122661
- average recall : 0.145557781925
- average f1 of : 0.0791289511813

# LDA topic model and user_item based hybrid recommender

topic_num = 50, user_items > 20

## neighbors = 50, recommend_item = 20
- average precision of hybird recommend method : 0.089501039501
- average recall of hybird recommend method : 0.0770532882419
- average f1 of hybird recommend method : 0.0680033405235

## neighbors = 50, recommend_item = 30
- average precision of hybird recommend method : 0.0852390852391
- average recall of hybird recommend method : 0.106597162755
- average f1 of hybird recommend method : 0.0771964004973

## neighbors = 50, recommend_item = 50
- average precision of hybird recommend method : 0.0775051975052
- average recall of hybird recommend method : 0.158019010317
- average f1 of hybird recommend method : 0.0856968289743

