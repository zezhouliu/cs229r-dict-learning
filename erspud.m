function [A obj] = learn_orthobasis_adm( Y, A_init, MAX_ITER, TOL, tau)

%%%
%
% erspud.m
%
% Uses ER-SpUD to Learn a sparsifying orthobasis.
%
%%%

done = false;
iter = 0;

dim = size(Y, 1);

A_old = A_init;

while ~done,

	iter = iter + 1;

    X = prox_L1(A_old' * Y, tau );
    A_new = proj_orthogonal_group( Y * X');

    stepSize = norm(A_old - A_new, 'fro');


    if stepSize < TOL * sqrt(dim) || iter >= MAX_ITER,
    	done = true;
    end

    A_old = A_new;
end

A = A_new;
obj = 0.5*norm(A'*Y - X,'fro')^2 + tau*norm(vec(X),1);
