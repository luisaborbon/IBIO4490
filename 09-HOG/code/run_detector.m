% Starter code prepared by James Hays for CS 143, Brown University
% This function returns detections on all of the images in a given path.
% You will want to use non-maximum suppression on your detections or your
% performance will be poor (the evaluation counts a duplicate detection as
% wrong). The non-maximum suppression is done on a per-image basis. The
% starter code includes a call to a provided non-max suppression function.
function [bboxes, confidences, image_ids] = .... 
    run_detector(test_scn_path, w, b, feature_params)
% 'test_scn_path' is a string. This directory contains images which may or
%    may not have faces in them. This function should work for the MIT+CMU
%    test set but also for any other images (e.g. class photos)
% 'w' and 'b' are the linear classifier parameters
% 'feature_params' is a struct, with fields
%   feature_params.template_size (probably 36), the number of pixels
%      spanned by each train / test template and
%   feature_params.hog_cell_size (default 6), the number of pixels in each
%      HoG cell. template size should be evenly divisible by hog_cell_size.
%      Smaller HoG cell sizes tend to work better, but they make things
%      slower because the feature dimensionality increases and more
%      importantly the step size of the classifier decreases at test time.

% 'bboxes' is Nx4. N is the number of detections. bboxes(i,:) is
%   [x_min, y_min, x_max, y_max] for detection i. 
%   Remember 'y' is dimension 1 in Matlab!
% 'confidences' is Nx1. confidences(i) is the real valued confidence of
%   detection i.
% 'image_ids' is an Nx1 cell array. image_ids{i} is the image file name
%   for detection i. (not the full path, just 'albert.jpg')

% The placeholder version of this code will return random bounding boxes in
% each test image. It will even do non-maximum suppression on the random
% bounding boxes to give you an example of how to call the function.

test_scenes = dir( fullfile( test_scn_path, '*.jpg' ));

%initialize these as empty and incrementally expand them.
bboxes = zeros(0,4);
confidences = zeros(0,1);
image_ids = cell(0,1);
cell_size = feature_params.hog_cell_size;
% scales = [1.5,1.25,1,0.85,0.75,0.5,0.25,0.15,0.1,0.05];
 scales = [1,0.85,0.75,0.6,0.5,0.4,0.25,0.15,0.1,0.07];
%scales = [0.85,0.75,0.5,0.25,0.15,0.1,0.07];
% scales = 0.65;
for i = 1:length(test_scenes)
      
    fprintf('Detecting faces in %s\n', test_scenes(i).name)
    img = imread(fullfile( test_scn_path, test_scenes(i).name ));
    img = single(img)/255;
    if(size(img,3) > 1)
        img = rgb2gray(img);
    end
    cur_bboxes = zeros(0,4);
    cur_confidences = zeros(0,1);
    cur_image_ids = cell(0,1);
    for scale = scales
        img_scaled = imresize(img, scale);
        [h, w] = size(img_scaled);    

        test_features = vl_hog(img_scaled, feature_params.hog_cell_size);
        img_num_cell_x = floor(w/feature_params.hog_cell_size);
        img_num_cell_y = floor(h/feature_params.hog_cell_size);

        temp_num_cell = feature_params.template_size / cell_size;

        num_window_x = img_num_cell_x - temp_num_cell + 1;
        num_window_y = img_num_cell_y - temp_num_cell + 1;

        D = temp_num_cell^2*31;
        window_feats = zeros(num_window_x * num_window_y, D);
        for x = 1:num_window_x
            for y = 1:num_window_y
                window_feats((x-1)*num_window_y+ y,:) = reshape(test_features(y:(y+temp_num_cell-1),x:(x+temp_num_cell-1),:), 1,D);
            end
        end
        scores = window_feats*w+b;
        indices = find(scores>0.80); % Selection of the best detections
        curscale_confidences = scores(indices);

        detected_x = floor(indices./num_window_y);
        detected_y = mod(indices, num_window_y)-1;
        curscale_bboxes = [cell_size*detected_x+1, cell_size*detected_y+1, ...
            cell_size*(detected_x+temp_num_cell), cell_size*(detected_y+temp_num_cell)]./scale;
        curscale_image_ids = repmat({test_scenes(i).name}, size(indices,1), 1);
       
        cur_bboxes = [cur_bboxes; curscale_bboxes];
        cur_confidences = [cur_confidences;curscale_confidences];
        cur_image_ids = [cur_image_ids; curscale_image_ids];
    end

    %NonMax Suppresion
    [max] = non_max_supr_bbox(cur_bboxes,cur_confidences, size(img));

    cur_confidences = cur_confidences(max,:);
    cur_bboxes = cur_bboxes(max,:);
    cur_image_ids = cur_image_ids(max,:);
    bboxes = [bboxes; cur_bboxes];
    confidences = [confidences; cur_confidences];
    image_ids = [image_ids; cur_image_ids];
end