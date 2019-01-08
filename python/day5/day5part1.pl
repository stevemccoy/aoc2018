% List concatenation.
conc([], L, L).
conc([H | Tail], L1, [H | L2]) :-
	conc(Tail, L1, L2).

process([],[],0).
process([C1, C2 | Tail], Product, N) :-
	D is C1 - C2,
	abs(D, 32),
	!,
	process(Tail, Product, N0),
	N is N0 + 1.
process([C1 | Tail], [C1 | Product], N) :-
	process(Tail, Product, N).


display_progress(Codes, Reductions) :-
	string_codes(S, Codes),
	write(Reductions),nl,
	write(S),
	nl.

render(L, Final) :-
	process(L, L2, N),
	N > 0,
	!,
	render(L2, Final).
render(L, L).


% working_directory(_, 'c:/src/github/fun/aoc2018/python/day5/').

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

