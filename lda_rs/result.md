# LDA topic model and tag-based hybrid recommender

- 50 topic for LDA model

## recommend 50 item with 30 similar users
- average precision : 0.055369595537
- average recall : 0.169104151485
- average f1 : 0.0655127241936

## recommend 30 item with 10 similar users
- average precision : 0.0575081357508
- average recall : 0.10599960863
- average f1 : 0.0575075305653

## recommend 30 item with 50 similar users
- average precision : 0.0629939562994
- average recall : 0.122295508481
- average f1 : 0.063406292959

-- filter user_items > 20
## recommend 50 item with 50 similar users
- average precision : 0.0722661122661
- average recall : 0.145557781925
- average f1 of : 0.0791289511813


# LDA topic model recommender(-- filter user_items > 20)

- average precision : 0.0609563409563
- average recall : 0.112909214625
- average f1 : 0.0649452142284


# Tag based user-similar recommender(-- filter user_items > 20)

- average precision : 0.0779625779626
- average recall : 0.160449822302
- average f1 : 0.0859543965989