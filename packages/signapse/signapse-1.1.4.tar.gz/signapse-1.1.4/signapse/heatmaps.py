import torch, copy, cv2, math, os
import numpy as np
from scipy import stats
import signapse.constants as C
# from signapse.logo import LOGO
from torchvision import transforms 
from torch.autograd import Variable
import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh
# import matplotlib.pyplot as plt

# Draw a line between two points using OpenCV, if they are positive points
def draw_line(im, joint1, joint2, c=(0, 0, 255),t=1,width=3,decimal_places=2):
    thresh = 0
    joint1 = (round(joint1[0].item(), decimal_places), round(joint1[1].item(), decimal_places))
    joint2 = (round(joint2[0].item(), decimal_places), round(joint2[1].item(), decimal_places))
    if joint1[0] > thresh and  joint1[1] > thresh and joint2[0] > thresh and joint2[1] > thresh:
        center = (int((joint1[0] + joint2[0]) / 2), int((joint1[1] + joint2[1]) / 2))
        length = int(math.sqrt(((joint1[0] - joint2[0]) ** 2) + ((joint1[1] - joint2[1]) ** 2))/2)
        angle = math.degrees(math.atan2((joint1[0] - joint2[0]),(joint1[1] - joint2[1])))
        cv2.ellipse(im, center, (width,length), -angle,0.0,360.0, c, -1)
        
def draw_line_nonan(im, joint1, joint2, c=(0, 0, 255),t=1, width=3):
    if not (joint1.isnan().any() or joint2.isnan().any()):
        draw_line(im, joint1, joint2, c, t, width)
        
def draw_face_mesh_small_tensor(frame,FM_tensor,connections=mp_face_mesh.FACEMESH_TESSELATION):
    for connection in connections:
        start_idx = connection[0]
        end_idx = connection[1]

        start = (FM_tensor[start_idx][0].item(),FM_tensor[start_idx][1].item())
        end = (FM_tensor[end_idx][0].item(), FM_tensor[end_idx][1].item())

        cv2.line(frame, start,end,color=(1, 1, 1), thickness=1)
    return frame
        
# Convert from a tensor representation to an image
def tensor2im(image_tensor, imtype=np.uint8, normalize=True):
    if isinstance(image_tensor, list):
        image_numpy = []
        for i in range(len(image_tensor)):
            image_numpy.append(tensor2im(image_tensor[i], imtype, normalize))
        return image_numpy
    image_numpy = image_tensor.cpu().float().numpy()
    if normalize:
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    else:
        image_numpy = np.transpose(image_numpy, (1, 2, 0)) * 255.0
    image_numpy = np.clip(image_numpy, 0, 255)
    if image_numpy.shape[2] == 1 or image_numpy.shape[2] > 3:
        image_numpy = image_numpy[:,:,0]
    return image_numpy.astype(imtype)     
            
class HEATMAPS():
    def __init__(self):
        super(HEATMAPS,self).__init__()
        
    def get_face_crop(self,image,face_landmarks,box=False,gray = True):
        face_oval = list(mp_face_mesh.FACEMESH_FACE_OVAL)
        width, height = image.shape[1],image.shape[0]
        cropped_frame = np.zeros_like(image)

        if box:
            x_min, y_min = width, height
            x_max, y_max = 0, 0
            for landmark in face_landmarks:
                x, y = int(landmark[0] * width ), int(landmark[1] * height)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)            
            cropped_frame[y_min:y_max, x_min:x_max] = image[y_min:y_max, x_min:x_max]
        else:
            routes_idx=[]
            p1 = [pair[0]for pair in face_oval]
            p2 = [pair[1]for pair in face_oval]
            #init_p1 = p1[0]
            init = p2[0]
            for _ in range(len(face_oval)):
                index = p1.index(init)
                init = p2[index]                
                routes_idx.append((p1[index],p2[index]))

            routes=[]
            for source_idx, target_idx in routes_idx:
                source = face_landmarks[source_idx]
                target = face_landmarks[target_idx]

                relative_source = (int(image.shape[1] * source[0]), int(image.shape[0] * source[1]))
                relative_target = (int(image.shape[1] * target[0]), int(image.shape[0] * target[1]))
                routes.append(relative_source)
                routes.append(relative_target) 

            mask = np.zeros((image.shape[0], image.shape[1]))                          
            mask = cv2.fillConvexPoly(mask,np.array(routes),1)
            mask = mask.astype(bool)
            cropped_frame[mask] = image[mask]
            if gray:
                cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            return cropped_frame 
    
        
    def skin_detection(self,frame,signer,include_hair= False):  
        space = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)
        if signer =="Marcel":
            lower_skin = np.array([60, 150, 77])   
            upper_skin = np.array([255, 190, 120])  
        elif signer =="Jay":
            lower_skin = np.array([60, 120, 77])   
            upper_skin = np.array([255, 255, 127]) 
            
        elif signer =="Rachel":
            # sharp to seprate the hair
            if include_hair:
                lower_skin = np.array([50, 130, 90])  
                upper_skin = np.array([220, 190, 125]) 
            else:                
                lower_skin = np.array([145, 131, 103])   # 145, 131, 103
                upper_skin = np.array([255, 190, 126]) 
   
        else:
            raise TypeError("Please set the signer into Marcel, Rachel or Jay. Skin_detection function in utils.py") 
        
        mask = cv2.inRange(space, lower_skin, upper_skin)
        # remove noise        
        # mask = cv2.erode(mask, np.ones((3,3), np.uint8), iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8), iterations=1)
        # mask = cv2.dilate(mask, np.ones((5,5), np.uint8), iterations=1)
        skin = cv2.cvtColor(cv2.bitwise_and(frame, frame, mask=mask), cv2.COLOR_BGR2GRAY)
        return skin 
    
    def get_edge(self,input_img):
        input_array = torch.clamp((input_img + 1) * 127.5, 0, 255).byte()
        np_img = input_array[0].cpu().numpy()       
        grad_x = cv2.Sobel(np_img, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(np_img, cv2.CV_64F, 0, 1, ksize=3)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        edges = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0) 
        edge_tensor =  torch.tensor(edges, dtype=torch.float32) / 255.0 * 2.0 - 1.0
        return edge_tensor.unsqueeze(0)
    

    def Rachel_hair_removal(self,face,hand,skin):
        face[face !=0] = 1
        hand[hand !=0] = 1
        mask = hand + face
        mask[mask > 1] = 1                
        mask = cv2.erode(mask[0], np.ones((5,5), np.uint8), iterations=1)
        mask = cv2.dilate(mask, np.ones((5,5), np.uint8), iterations=1)[np.newaxis,...]       
        return mask * skin

    def find_bounding_box(self,image):
        mini = np.min(image)
        # Find the coordinates of non-zero pixels
        non_zero_pixels = np.argwhere(image > mini)
        
        if non_zero_pixels.size == 0:
            # No non-zero pixels found
            return None

        # Get the minimum and maximum coordinates
        y_min, x_min = np.min(non_zero_pixels, axis=0)
        y_max, x_max = np.max(non_zero_pixels, axis=0)
        
        # Define the bounding box coordinates
        bounding_box = (x_min, y_min, x_max, y_max)        
        return bounding_box
    
    def crop_hand_gray_normalised(self,args, frame, frame_no, hand,face_mask):
        if args.opt.hand_crop:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hand = (gray*hand).astype('uint8')[0] /255
            hand_mask = np.expand_dims(hand,axis=0)
            if args.opt.hand_edge:
                hand = np.array(self.get_edge(torch.from_numpy(hand_mask)))                      
                    
        if args.opt.face_crop:
            face = self.get_face_crop(frame,face_mask)/255 
            face_mask = np.expand_dims(face,axis=0)       
            if args.opt.face_edge:
                face = np.array(self.get_edge(torch.from_numpy(face_mask)))
        
        if args.opt.skin_crop:
            skin = self.skin_detection(frame,args.opt.signer,include_hair = False) /255  #(SAM_face or SAM_hand)
            skin_mask = np.expand_dims(skin,axis=0)
            if args.opt.skin_edge:
                skin = np.array(self.get_edge(torch.from_numpy(skin_mask)))           
                
        # if SAM_hand and SAM_face and SAM_skin:
        if args.opt.signer == "Rachel" and args.opt.hand_crop and args.opt.face_crop and args.opt.skin_crop:
            if os.path.exists(args.saving_file_path):
                face_mask_zeros = np.zeros_like(face_mask)
                skin = self.Rachel_hair_removal(face_mask_zeros,hand_mask,skin_mask)
                skin = np.array(self.get_edge(torch.from_numpy(skin)))  
                # Load the NumPy file
                data = np.load(args.saving_file_path)
                if frame_no < len(data):
                    mask_zeros = np.full_like(skin, -1)
                    # TODO compute these numbers auto
                    mask_zeros[:,160:430,400:630] = data[frame_no]/3
                    # mask_zeros = mask_zeros + skin
                    skin = np.where(skin > -1, skin, mask_zeros)  
            else:
                skin = self.Rachel_hair_removal(face_mask,hand_mask,skin_mask)
                skin = np.array(self.get_edge(torch.from_numpy(skin)))  
            return skin
            
        if args.opt.hand_crop and args.opt.face_crop:
            return (np.concatenate((hand, face)))
        elif args.opt.skin_crop:
            return skin  
        elif args.opt.hand_crop:
            return hand
        elif args.opt.face_crop:
            return face  
        else:    
            raise TypeError("Please set the correct flags for SAM hand and face masks")
    
    def update_position(slef, point, msk):
        points_with_value_1 = torch.nonzero(torch.from_numpy(msk) == 1, as_tuple=False).to(point.device)
        distances = torch.sqrt((points_with_value_1[:, 0] - point[0])**2 + (points_with_value_1[:, 1] - point[1])**2)
        min_index = torch.argmin(distances)
        # points_with_value_1 = np.argwhere(msk == 1)
        # distances = np.sqrt((points_with_value_1[:, 0] - point[0])**2 + (points_with_value_1[:, 1] - point[1])**2)
        # min_index = np.argmin(distances)

        point = points_with_value_1[min_index]
        return point

    def adjust_wrists(self, x , left, right):
        device = left.device
        pixels = x.reshape((-1, 1))
        dominant_color = stats.mode(pixels, axis=0)[0][0]
        x[x>dominant_color] = 1
        x[x<1] = 0
        x = cv2.dilate(x, np.ones((5,5), np.uint8), iterations=1)
        if left.max() <= 1024 and x[int(left[1].item()),int(left[0].item())] == 0:
            left = self.update_position(left , x)
        if right.max() <= 1024 and x[int(right[1].item()),int(right[0].item())] ==0:
            right = self.update_position(right , x)
        return left.to(device), right.to(device)




    def get_heatmaps_crops(self,input_frame,MP_results_gen,GAN_model, args,iii=0, hand_mask=None,face_mask=None):
        resolution = args.opt.loadSize
        MP_results_gen = MP_results_gen*resolution 
        if args.opt.sam: # do sam
            cropped_hand = self.crop_hand_gray_normalised(args,input_frame, iii,hand_mask,face_mask)
            MP_results_gen[4], MP_results_gen[5] = self.adjust_wrists(copy.copy(cropped_hand[0]), MP_results_gen[4], MP_results_gen[5])

        # First, create a HeatMap representation from the MediaPipe tensor
        results_pose = MP_results_gen[:6]
        results_LH = MP_results_gen[6:27]
        results_RH = MP_results_gen[27:48]
        results_face = MP_results_gen[48:176]
        results_hip = MP_results_gen[176:]

        face_connections = C.FACE_CONNECTIONS_SAM
        heat_map_dim = 5 + 40 + len(face_connections) + 3
        heat_map = np.zeros((heat_map_dim, resolution, resolution), np.uint8)
        

        # MP Body
        draw_line_nonan(heat_map[0], (results_pose[0]), (results_pose[1]), c=(1, 1, 1), t=1, width=1)
        # Left
        draw_line_nonan(heat_map[1], (results_pose[0]), (results_pose[2]), c=(1, 1, 1), t=1, width=1)
        # draw_line_nonan(heat_map[2], (results_pose[2]), (results_pose[4]), c=(1, 1, 1), t=1, width=1)
        draw_line_nonan(heat_map[2], (results_pose[2]), (results_LH[0]), c=(1, 1, 1), t=1, width=1)
        # Right
        draw_line_nonan(heat_map[3], (results_pose[1]), (results_pose[3]), c=(1, 1, 1), t=1, width=1)
        # draw_line_nonan(heat_map[4], (results_pose[3]), (results_pose[5]), c=(1, 1, 1), t=1, width=1)
        draw_line_nonan(heat_map[4], (results_pose[3]), (results_RH[0]), c=(1, 1, 1), t=1, width=1)

        # MP Hands
        for i in range(5):
            draw_line_nonan(heat_map[4 + 4 * i + 1], (results_LH[0]), (results_LH[i * 4 + 1]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[4 + 4 * i + 2], (results_LH[i * 4 + 1]), (results_LH[i * 4 + 2]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[4 + 4 * i + 3], (results_LH[i * 4 + 2]), (results_LH[i * 4 + 3]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[4 + 4 * i + 4], (results_LH[i * 4 + 3]), (results_LH[i * 4 + 4]), c=(1, 1, 1), t=1, width=1)

        for i in range(5):
            draw_line_nonan(heat_map[24 + 4 * i + 1], (results_RH[0]), (results_RH[i * 4 + 1]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[24 + 4 * i + 2], (results_RH[i * 4 + 1]), (results_RH[i * 4 + 2]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[24 + 4 * i + 3], (results_RH[i * 4 + 2]), (results_RH[i * 4 + 3]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[24 + 4 * i + 4], (results_RH[i * 4 + 3]), (results_RH[i * 4 + 4]), c=(1, 1, 1), t=1, width=1)

        ## FACE
        for c, connection in enumerate(face_connections):
            new_connection = (GAN_model.face_points[connection[0]], GAN_model.face_points[connection[1]])
            draw_line_nonan(heat_map[45 + c], (results_face[new_connection[0]]), (results_face[new_connection[1]]), c=(1, 1, 1), t=1, width=1)

        # MP Hip
        draw_line(heat_map[169], results_hip[0],  results_hip[1], c=(1, 1, 1), t=1, width=1)
        draw_line(heat_map[170], results_hip[0], results_pose[0], c=(1, 1, 1), t=1, width=1)
        draw_line(heat_map[171], results_hip[1], results_pose[1],  c=(1, 1, 1), t=1, width=1)      
        
 
        if not torch.is_tensor(heat_map):
            heat_map = torch.tensor(heat_map)
            
        heat_map_2 = copy.copy(heat_map)    
        # set poses       
        heat_map =[]
        if not args.opt.remove_body_pose:
            heat_map.append(heat_map_2[:5])    
                
        if not args.opt.remove_hand_pose:
            heat_map.append(heat_map_2[5:45]) 
            
        if not args.opt.remove_face_pose:
            heat_map.append(heat_map_2[45:169])
                                
        if not args.opt.remove_hip_pose:
            heat_map.append(heat_map_2[169:172])
                        
        heat_map = np.concatenate(heat_map, axis=0)

        # face_mesh
        if args.opt.face_mesh:
            heat_map = np.concatenate((heat_map, heat_map_2[-1:]), axis=0) 

        if args.opt.sam:
            # do sam
            # cropped_hand = self.crop_hand_gray_normalised(args,input_frame, iii,hand_mask,face_mask)
                
            # Normalisation
            if args.opt.crop_normalise:
                handcrop_transform = transforms.Compose([transforms.Normalize((0.5,), (0.5,))])
                if args.opt.hand_crop and args.opt.face_crop and args.opt.skin_crop:
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
                elif args.opt.hand_crop and args.opt.face_crop:
                    cropped_hand[1] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[1].astype('float16')).unsqueeze(dim=0)))
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
                elif args.opt.hand_crop:
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
                elif args.opt.face_crop : #and not opt.signer =="Rachel"
                    cropped_hand[1] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[1].astype('float16')).unsqueeze(dim=0)))
                else:
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
            if not torch.is_tensor(cropped_hand):
                cropped_hand = torch.tensor(cropped_hand) 
        else:
            cropped_hand = None

        # After you've created heatmap label, Concetenate the base image tensor on to the front
        if not torch.is_tensor(heat_map):
            heat_map = torch.tensor(heat_map)            

        return heat_map,cropped_hand
    
    # Convert a heatmap representation to an image
    def convert_limb_heatmap(self,heat_map,imtype=np.uint8):
        heat_map = np.array(heat_map)
        full_heatmap = np.zeros((heat_map.shape[1], heat_map.shape[2]), imtype)
        for frame in heat_map:
            full_heatmap = np.add(full_heatmap,frame)  #full_heatmap + frame
        full_heatmap = ((full_heatmap != 0) == False)*255
        return full_heatmap.astype(imtype)
    
    
    def get_pose_image(self,opt,input_frame,generated,heat_map,crops):
        if opt.sam:            
            if opt.multi_frames:
                total_maps_per_sample = (len(heat_map)//((opt.num_frames*2)+1)) - len(crops[0])
                input_label = self.convert_limb_heatmap(heat_map[opt.num_frames*total_maps_per_sample:(opt.num_frames+1)*total_maps_per_sample,:,:]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            
            elif (opt.hand_crop and opt.face_crop) and not opt.skin_crop:
                input_label = self.convert_limb_heatmap(heat_map[:-2]).reshape((heat_map.shape[1], heat_map.shape[2], 1))            
            else:
                input_label = self.convert_limb_heatmap(heat_map[:-1]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            
                

            if  opt.crop_normalise:
                avg_bg = -int(crops[0][0][:10,:10].mean()) # to keep the background zeros
                if opt.erusion:
                    hand = (crops[0][0].numpy() + avg_bg ) * 255
                    if not opt.merge_crops:
                        body = (crops[0][1].numpy() + avg_bg ) * 255
                else:
                    hand = (crops[0][0].numpy()+ avg_bg) * 255
                    # if (opt.hand_crop and opt.face_crop) and not opt.skin_crop :
                    #     body = (crops[0][1].numpy()+ avg_bg) * 255
                    #     body[body==0]=255
                hand[hand==0]=255             
 
                
                if (opt.hand_crop and opt.face_crop) and not (opt.skin_crop or opt.merge_crops):
                    input_label[:,:,0] = (input_label[:,:,0]) + (255 - (hand).astype(np.uint8))  + (255-(body).astype(np.uint8)) 
                else:
                    input_label[:,:,0] = (255* ((input_label[:,:,0])/255 *  (hand).astype(np.uint8)/255)) #(255 - (hand).astype(np.uint8)) 
                             
                    
            else: 
                if (opt.hand_crop and opt.face_crop) and not (opt.skin_crop or opt.merge_crops):                              
                    input_label[:,:,0] = input_label[:,:,0] + (heat_map[-2]*255).numpy().astype(np.uint8) + (heat_map[-1]*255).numpy().astype(np.uint8)
                else:
                    input_label[:,:,0] = input_label[:,:,0] + (heat_map[-1]*255).numpy().astype(np.uint8)
                    
                
        elif opt.hand_crop or opt.face_crop or opt.skin_crop:
            if opt.N2N:
                input_label = self.convert_limb_heatmap(heat_map).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            elif opt.multi_frames:
                total_maps_per_sample = (len(heat_map)//((opt.num_frames*2)+1)) - len(crops[0])
                input_label = self.convert_limb_heatmap(heat_map[opt.num_frames*total_maps_per_sample:(opt.num_frames+1)*total_maps_per_sample,:,:]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            else:
                input_label = self.convert_limb_heatmap(heat_map[:-1]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            if opt.crop_normalise:
                if opt.hand_crop or opt.skin_crop:
                    hand = (crops[0].numpy() +1 ) * 255               
                    hand[hand==0]=255                    
                    input_label[:,:,0] = input_label[:,:,0] + (255 - (hand).astype(np.uint8))
                else :
                    if opt.erusion:
                        body = (crops[1].numpy() +1 ) * 255
                    else:
                        body = crops[1].numpy() * 255                    
                    body[body==0]=255
                    input_label[:,:,0] = input_label[:,:,0] + (255-(body).astype(np.uint8)) 
            else:            
                input_label[:,:,0] = input_label[:,:,0] + (heat_map[-1]*255).numpy().astype(np.uint8)          

        else:                    
            input_label = self.convert_limb_heatmap(heat_map).reshape((heat_map.shape[1], heat_map.shape[2], 1))
                
        input_label = np.concatenate((input_label, input_label, input_label), axis=2)
        pose_image = np.ascontiguousarray(input_label)[:, :opt.loadSize]
        pose_image = cv2.cvtColor(pose_image, cv2.COLOR_BGR2RGB)
        input_frame = cv2.resize(input_frame, dsize=(opt.loadSize, opt.loadSize),
                                    interpolation=cv2.INTER_CUBIC)
        output_frame = np.concatenate((input_frame, pose_image, generated), axis=1)

        return output_frame

    def generate_GAN_frame_maps_crops(self,input_frame,maps,crops,GAN_model,opt,detailed_video=False):    
        if crops[0] == None:
            heat_map = np.concatenate(maps, axis=0)  
        else:
            heat_map = np.concatenate((np.concatenate(maps, axis=0), np.concatenate(crops, axis=0)), axis=0)  
               
        # After you've created heatmap label, Concetenate the base image tensor on to the front
        if not torch.is_tensor(heat_map):
            heat_map = torch.tensor(heat_map)
            
        if GAN_model.opt.base_style:
            torch_label = torch.cat((GAN_model.base_tensor, heat_map.float().unsqueeze(0)), dim=1).unsqueeze(0)
        else:
            torch_label = heat_map.float().unsqueeze(0).unsqueeze(0)
        # After you've created the full heatmap label, pass it through to the GAN model
        with torch.no_grad():
            gen = GAN_model.forward(Variable(torch_label),face=None)
            if len(gen) > 3:
                output_frame = []
                n = int((len(gen)/3) / 2)
                generated = gen[3*n:3*(n+1)]
                generated = np.ascontiguousarray(tensor2im(generated))
                if detailed_video:  
                    output_frame = self.get_pose_image(opt,input_frame,generated,maps[n],crops[n])  
                else:
                    output_frame = generated 
                
            else:
                generated = np.ascontiguousarray(tensor2im(gen))
                if detailed_video:      
                    output_frame = self.get_pose_image(opt,input_frame,generated,heat_map,crops)  
                else:
                    output_frame = generated       
        return output_frame     
    
