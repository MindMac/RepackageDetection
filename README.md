# RepackageDetection
A Script to detect if the Android application is repackaged based on the method proposed by the paper "[Exploring reverse engineering symptoms in Android apps](http://dl.acm.org/citation.cfm?id=2751330)". It seems the *string offset* feature is not applicable for the Android application repackaged by the lateset Apktool(2.0.0).

##Usage
python repackage_detection.py -f \<apk_file_path\>
