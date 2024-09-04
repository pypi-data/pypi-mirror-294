import pydicom
#
path = "/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/all_fields_data/all_fields_file.dcm"
# path = "/localscratch/Users/cavriley/dcm_classifier_issue/t2_error/MR000013.dcm"
ds = pydicom.dcmread(path)

print("before")
print(ds)
# #
# ds["ContrastBolusAgent"].value = ""
# ds["InversionTime"].value = None
# ds["SAR"].value = None
#
# print("after")
# print(ds)
#
# ds.save_as("/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/all_fields_data/empty_fields.dcm")
