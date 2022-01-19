diary Nilabh_lab3_diary.txt 
echo on
% #1 - defining a mini web 
echo off 
A = [1 0 1 0 0 0 1; 1 1 0 0 1 1 0; 1 0 1 0 0 1 0; 1 1 1 1 0 1 0; 0 1 1 1 1 1 1; 0 0 0 1 1 1 0; 0 1 0 1 0 1 1]
P = bsxfun(@rdivide, A, sum(A))
echo on
% #2 - Crawling the web from site 1 and printing "location" at timestep 1
% and 2
echo off
x0 = [1 0 0 0 0 0 0];
x0 = x0(:);
x1 = P * x0
x2 = P * time_1
echo on
% #3 - printing location of crawlers starting at site one for different
% time steps using for loop
echo off 
for j=1:50
x = (P ^ j) * x0;
    if j == 5
        fprintf('x5 \n' )
        disp(x)
    elseif j == 10
        fprintf('x10 \n' )
        disp(x)
    elseif j == 20
        fprintf('x20 \n' )
        disp(x)
    elseif j == 50 
        fprintf('x50 \n' )
        disp(x)
    end
end
echo on
% #4 - changing starting vector to being equally distributed and repeating
% process from #3 to observe changes in behavior based on new location
% vectors. 
echo off 
x0 = [1 1 1 1 1 1 1];
x0 = x0(:);
for j=1:50
x = (P ^ j) * x0;
    if j == 1
        fprintf('x1 \n' )
        disp(x)
    elseif j == 2
        fprintf('x2 \n')
        disp(x)
    elseif j == 10
        fprintf('x10 \n' )
        disp(x)
    elseif j == 20
        fprintf('x20 \n' )
        disp(x)
    elseif j == 50 
        fprintf('x50 \n' )
        disp(x)
    end
end
echo on
% #5 - computing steady state q of probability matrix, aka the page rank
% vector. q is then normalized to sum to 7, the number of sites in our mini
% web. The site with the highest page rank is site 5, while the one with
% the lowest page rank is site 3. 
echo off 
[V,D]=eig(P);
q = [-0.2153 -0.4223 -0.1491 -0.3395 -0.6148 -0.3478 -0.3726];
q = q(:);
q = q/sum(q);
q = q*7
fprintf('5 has the highest page rank \n')
fprintf('3 has the lowest page rank \n')
echo on 
% #6 - finding how we get highest page rank
% 6a. finding in degree nodes by multiplying adjacency matrix by column
% vector of ones (sums of each row) 
% 6b. Finding out degree nodes by getting sums of each row
% 6c. sorting page rank and din and dout in descending order 
% seems to show that the page rank has a strong positive association with
% the number of in degree nodes and a slight negative association with out
% degree nodes 
echo off 
din = A * x0
R1 = x0.';
dout = R1 * A
 
[qsorted, Ivec] = sort(q, 'descend')
din_sorted = din(Ivec)
dout_sorted = dout(Ivec)
echo on
% #7 - The site with the lowest page rank is site 3, as discussed earlier.
% Therefore, to raise the page rank of this website, we will add an edge
% between the 5th website. with the highest page rank, and the 3rd website,
% as this would increase the in degree nodes while connecting from the most
% popular website in our mini-web. From the results, we can see that the
% page rank of the 3rd website goes from last to 4th, meaning this change
% worked. Below. I print the steady state vector r and the sorted version.  
echo off 
B = [1 0 1 0 0 0 1; 1 1 0 0 1 1 0; 1 0 1 0 1 1 0; 1 1 1 1 0 1 0; 0 1 1 1 1 1 1; 0 0 0 1 1 1 0; 0 1 0 1 0 1 1];
Q = bsxfun(@rdivide, B, sum(B));
[W,E]=eig(Q);
r = [0.2698 0.3469 0.3469 0.3854 0.5781 0.2891 0.3469];
r = r(:)
[rsorted, Pvec] = sort(r, 'descend')
echo on 
% #8 - Adding a damping factor and finding steady state vectors for
% resulting P-hat matrices. The results show that adding a higher dampening
% factor results in the pagerank values getting closer, which concurs with
% the idea of web crawlers choosing sites randomly. 
echo off 
P_85 = 0.85 * P + .15/7;
[V,D]= eig(P_85);
q_85 = V(:,1);
q_85 = (q_85 / sum(q_85)) * 7
 
P_95 = 0.95 * P + .05/7;
[V,D]= eig(P_95);
q_95 = V(:,1);
q_95 = (q_95 / sum(q_95)) * 7
 
P_75 = 0.75 * P + .25/7;
[V,D]= eig(P_75);
q_75 = V(:,1);
q_75 = (q_75 / sum(q_75)) * 7

