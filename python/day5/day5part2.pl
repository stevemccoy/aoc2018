

% UTILITIES:

% List concatenation.
conc([], L, L).
conc([H | Tail], L1, [H | L2]) :-
	conc(Tail, L1, L2).

% Remove any instances of a value from a list.
remove_all(_, [], []).
remove_all(V, [V | Tail], TailAfter) :-
	!,
	remove_all(V, Tail, TailAfter).
remove_all(V, [H | Tail], [H | TailAfter]) :-
	remove_all(V, Tail, TailAfter).

% Remove all instances of each of the items in the middle list.
remove_all_of_items(L1, [], L1).
remove_all_of_items(L1, [V | Tail], L3) :-
	remove_all(V, L1, L2),
	remove_all_of_items(L2, Tail, L3).

% Zip the corresponding elements from two lists together.

zip_lists([], [], []).
zip_lists([Item1 | Tail1], [Item2 | Tail2], [[Item1, Item2] | ZippedTail]) :-
	length(Tail1, N),
	length(Tail2, N),
	zip_lists(Tail1, Tail2, ZippedTail).


% working_directory(_, 'c:/src/github/fun/aoc2018/python/day5/').


% READ THE INPUT DATA:

get_all_codes(S, [C | Tail]) :-
	get_code(S, C),
	C > -1,
	!,
	get_all_codes(S, Tail).
get_all_codes(S, []) :-
	at_end_of_stream(S).

get_day5_input(Codes) :-
	open('input.txt', read, S),
	get_all_codes(S, Codes),
	close(S).


% PROCESS THE DATA:

% Process the polymer once.
process([],[],0).
process([C1, C2 | Tail], Product, N) :-
	D is C1 - C2,
	abs(D, 32),
	!,
	process(Tail, Product, N0),
	N is N0 + 1.
process([C1 | Tail], [C1 | Product], N) :-
	process(Tail, Product, N).


% SHOW CODES AS A CHARACTER STRING:

display_progress(Codes, Reductions) :-
	string_codes(S, Codes),
	write(Reductions),nl,
	write(S),
	nl.


% REDUCE THE DATA AS FAR AS POSSIBLE:

% Repeat process the polymer until no more can be reduced.
render(L, Final) :-
	process(L, L2, N),
	N > 0,
	!,
	render(L2, Final).
render(L, L).


% Remove specified items and then render down the polymer.
reduced_rendering(L1, RemoveItems, Final, Length) :-
	remove_all_of_items(L1, RemoveItems, L2),
	render(L2, Final),
	length(Final, Length).

% Reduce down for renderings after removing both types of one letter from the input.
make_letter_code_pairs(Pairs) :-
	Alphabet = "abcdefghijklmnopqrstuvwxyz",
	string_codes(Alphabet, LowerCodes),
	string_upper(Alphabet, UpperAlpha),
	string_codes(UpperAlpha, UpperCodes),
	zip_lists(LowerCodes, UpperCodes, Pairs).


solution(Results) :-
	make_letter_code_pairs(Pairs),
	get_day5_input(AllCodes),
	findall(PS/Length, (
		member(Pair, [[] | Pairs]),
		reduced_rendering(AllCodes, Pair, _, Length),
		string_codes(PS, Pair)
	), Results).


