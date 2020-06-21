# accents = ['á', 'é', 'í', 'ó', 'ú']
# non_accents = ['a', 'e', 'i', 'o', 'u']
# for index, row in pecota.iterrows():
#     arr = list(row['name'])
#     for i in range(len(arr)):
#         for j in range(len(accents)):
#             if arr[i] == accents[j]:
#                 arr[i] = non_accents[j]
#     pecota.loc[index, 'name'] = ''.join(arr)
# pecota['name'] = pecota['first_name'] + ' ' + pecota['last_name']
