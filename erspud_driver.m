%Description of major subroutines
%================================
%preprocess.py : convert input textual review to sparse encoding
%erspud.m : learn an orthogonal sparsifying dictionary using erspud
%
%

clear all; clc;

num_trial_per_review = 100;

% parameters for erspud
MAX_ITER = 10000;
TOL = 1e-5;
tau = 2; 

addpath('test_slate');

Y = imread("reviewencoding.txt");

[m, p] = size(Y);

done = false;
all_obj = [];

rng(i, 42);  % to ensure reproducibility, we specify both the seed and the alg 

for j = 1:num_trial_per_review,

    [A obj_value] = learn_orthobasis_adm( Y, proj_orthogonal_group(randn(m,m)), MAX_ITER, TOL, tau);
    all_obj = [all_obj, norm1(A'*Y)];
%        allObj = [allObj, obj_value]; % objective values

    if j == 1,
        break
    end
    
    stem(all_obj);
    ylim([0, 1.25 * max(all_obj)]);
            
end
