# -*- coding: utf-8 -*-

import Id_Id.search_paths

id1 = 2157025439
id2 = 2102958620

# id1 = 2061901927
# id2 = 2134746982


path = Id_Id.search_paths.Id2Id().one_hop(id1, id2)
print 'one_hop_path:',path
path2 = Id_Id.search_paths.Id2Id().two_hop(id1, id2)
print 'two_hop_path:',path2