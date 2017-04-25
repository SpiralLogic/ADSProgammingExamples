# Eularian Circuit

This program takes an input of strings  of the same length and finds a eularian ciruit that connects them all
two strings are connected when the end of one string is the lame as the start of another

For example, these strings are connected (- is not part of the string):

Some Str---<br>
-ome Stri--<br>
--me Strin-<br>
---e String<br>

The output is the reconstruction of all of the strings from the input file

i.e.
Some Str
ome Stri
me Strin
e String

becomes: 
Some String


#### Example
python ecircuit.py wordstrings.txt 

# Complexities

Space complexity of vertices:
------------------------------

O(|V|) space is used to store each vertex and it's associated string
O(|E|) space is used to store each of the edges in a linked list where each index of the list
represents the vertex number

Total space used: O(|V| + |E|)

if the graph is sparse and |V| > |E| then space complexity will be O(|V|)

if the graph is dense and |E| > |V| then space complexity will be O(|E|)

Time complexity of generating graph
-----------------------------------

Using a known property of the graph being a De Bruijn graph we know that each vertex will have
M edges. Using this property vertices can be generated in O(|V| * m) time. This is done by
sorting the vertices or in the case of this implementation, generate the vertices already
sorted.

For graphs that aren't De Bruijn then graph generation will take O(|V|^2) complexity. For example
when loading from a string file.



Time complexity of finding the circuit
--------------------------------------

Time complexity of finding the circuit is O(|E| * checking for disconnect)

I am using a BFS to detect a disconnect each time there are more than 2 edges for a
vertex. This checking for disconnect takes O(|V| + |E|) as we need to go to each vertex
and need to go to each edge.

This makes my total complexity
O(|E| * (|V| + |E|))
= O(|V||E| + |E|^2)
= O(|E|^2)              (if |V| == |E| then, O(2|E|^2) which is still O(|E|^2)

If there was only 1 edge per vertex then the BFS would never occur. Which allows us to assume
that |V| < |E| as each vertex would then have less than 2 edges. If there was only 1 edge per vertex
then time complexity would be O(|E|) as checking for a disconnect would never occur (giving it
a time complexity of O(1)).


If I was more ambitious and actually finished implementing Trajan's algorithm then I could work out
the bridges in advanced to make checking for a disconnect possible in O(1).

Space complexity of finding the circuit
--------------------------------------

Space complexity for finding e-circuit
O(|V| + |E|)

When finding the disconnects via BFS it will only add 1 extra copy of O(|V|+|E|) so the
space complexity will not change while searching
"""

Example
--
<pre>
python ecircuit.py wordstrings.txt

Finding circuit...
E-circuit found!
[30, 506, 94, 378, 596, 194, 574, 390, 150, 692, 407, 316, 558, 621, 747, 4, 62, 186, 508, 111, 498, 9, 258, 428, 492, 313, 534, 653, 437, 552, 514, 177, 455, 41, 23, 267, 37, 19, 619, 718, 426, 453, 505, 92, 376, 594, 192, 572, 388, 115, 540, 356, 107, 480, 139, 664, 759, 489, 219, 551, 475, 637, 102, 442, 628, 54, 167, 79, 261, 441, 602, 292, 240, 672, 296, 248, 93, 377, 595, 193, 573, 389, 128, 604, 318, 581, 605, 343, 647, 314, 536, 703, 436, 531, 369, 123, 564, 726, 329, 608, 462, 197, 583, 632, 71, 212, 345, 711, 738, 301, 304, 509, 131, 649, 320, 585, 713, 308, 518, 228, 341, 638, 116, 541, 358, 136, 661, 756, 486, 216, 548, 472, 624, 11, 48, 31, 668, 98, 395, 204, 640, 127, 579, 566, 736, 1, 479, 8, 496, 3, 160, 732, 335, 615, 697, 418, 226, 338, 623, 5, 76, 237, 556, 535, 654, 446, 658, 702, 435, 530, 368, 114, 539, 355, 60, 179, 470, 459, 126, 578, 560, 657, 652, 417, 213, 464, 279, 106, 467, 312, 532, 380, 679, 381, 10, 510, 132, 650, 321, 586, 714, 309, 519, 229, 342, 639, 117, 542, 359, 143, 684, 399, 274, 89, 373, 450, 724, 305, 511, 137, 662, 757, 487, 217, 549, 473, 625, 15, 147, 688, 403, 283, 129, 643, 180, 490, 284, 135, 660, 755, 485, 215, 546, 458, 109, 483, 210, 748, 66, 196, 580, 568, 290, 198, 587, 110, 495, 722, 477, 704, 438, 577, 465, 285, 153, 700, 429, 494, 340, 636, 99, 430, 502, 56, 169, 130, 648, 319, 584, 712, 307, 517, 224, 264, 14, 52, 47, 29, 357, 121, 554, 525, 281, 118, 543, 360, 148, 689, 404, 288, 161, 733, 336, 616, 698, 419, 227, 339, 634, 74, 222, 185, 503, 70, 211, 272, 87, 353, 746, 582, 606, 344, 656, 645, 294, 245, 68, 203, 630, 65, 189, 533, 561, 693, 408, 324, 590, 158, 730, 333, 613, 677, 350, 743, 73, 221, 752, 133, 651, 411, 423, 365, 701, 434, 529, 367, 59, 178, 469, 457, 103, 449, 709, 641, 138, 663, 758, 488, 218, 550, 474, 633, 72, 220, 751, 122, 555, 526, 282, 125, 576, 461, 171, 225, 287, 155, 707, 538, 146, 687, 402, 278, 105, 466, 302, 363, 666, 63, 187, 520, 243, 57, 175, 252, 259, 433, 528, 366, 55, 168, 113, 527, 347, 737, 134, 659, 754, 484, 214, 545, 456, 69, 205, 669, 141, 682, 397, 271, 84, 310, 522, 250, 119, 544, 361, 152, 695, 412, 443, 642, 156, 728, 331, 611, 675, 348, 741, 6, 149, 691, 406, 306, 513, 145, 686, 401, 277, 104, 463, 209, 710, 674, 325, 591, 159, 731, 334, 614, 678, 351, 744, 96, 393, 201, 627, 53, 166, 78, 260, 440, 601, 291, 239, 671, 295, 246, 83, 300, 257, 371, 286, 154, 706, 537, 142, 683, 398, 273, 88, 362, 557, 609, 493, 323, 589, 157, 729, 332, 612, 676, 349, 742, 13, 51, 44, 26, 172, 230, 382, 40, 22, 266, 36, 18, 618, 717, 425, 452, 504, 91, 375, 593, 191, 571, 386, 97, 394, 202, 629, 61, 183, 500, 45, 27, 721, 468, 328, 607, 415, 182, 499, 39, 21, 439, 598, 242, 720, 447, 665, 33, 0, 165, 75, 235, 471, 559, 646, 298, 251, 124, 567, 206, 680, 392, 164, 740, 410, 420, 233, 391, 162, 735, 445, 655, 448, 708, 635, 81, 289, 173, 231, 384, 64, 188, 521, 247, 85, 346, 734, 337, 622, 749, 82, 299, 256, 370, 276, 100, 431, 512, 144, 685, 400, 275, 90, 374, 592, 190, 570, 385, 86, 352, 745, 174, 241, 705, 478, 750, 120, 553, 516, 223, 263, 2, 12, 50, 34, 16, 476, 696, 413, 562, 715, 372, 383, 42, 24, 268, 38, 20, 620, 719, 427, 454, 507, 95, 379, 597, 195, 575, 414, 631, 67, 199, 600, 280, 112, 515, 181, 491, 293, 244, 58, 176, 364, 673, 322, 588, 140, 681, 396, 269, 43, 25, 723, 670, 232, 387, 108, 481, 207, 690, 405, 303, 482, 208, 699, 421, 234, 416, 184, 501, 49, 32, 422, 236, 547, 460, 170, 200, 626, 46, 28, 565, 727, 330, 610, 667, 77, 253, 265, 35, 17, 617, 716, 424, 451, 497, 7, 151, 694, 409, 354, 753, 163, 739, 326, 599, 270, 80, 262, 444, 644, 238, 563, 725, 327, 603, 297, 249, 101, 432, 524, 255, 317, 569, 311, 523, 254, 315]

In_graph_theory,_an_n-dimensional_De_Bruijn_graph_of_m_symbols_is_a_directed_graph_representing_overlaps_between_sequences_of_symbols._It_has_pow(m,n)_vertices,_consisting_of_all_possible_length-n_sequences_of_the_given_symbols;_the_same_symbol_may_appear_multiple_times_in_a_sequence.__If_one_of_the_vertices_can_be_expressed_as_another_vertex_by_shifting_all_its_symbols_by_one_place_to_the_left_and_adding_a_new_symbol_at_the_end_of_this_vertex,_then_the_latter_vertex_has_a_directed_edge_to_the_former_vertex.__Each_De_Bruijn_graph_has_an_Eulerian_Circuit_(a_closed_path_which_visits_each_and_every_edge_in_the_graph_exactly_once).__Although_De_Bruijn_graphs_are_named_after_the_Dutch_mathematician_Nicolaas_Govert_de_Bruijn,_they_were_discovered_independently_by_I._J._Good</pre>
