# -- coding: utf-8 --

import numpy as np

# @Time : 2023/2/9 20:53
# @Author : Zhiheng Feng
# @File : generate_ply.py
# @Software : PyCharm


def xyz2ply(xyz,output_file, color):
    n = xyz.shape[0]
    colors = np.tile(color, [n, 1])
    if not output_file.endswith('.ply'):
        output_file = output_file + '.ply'
    create_output(xyz, colors, output_file)


def txt2ply(input_file, output_file, color):
    with open(input_file, 'rb') as fp:
        lines = fp.readlines()
        points = np.array([np.array([float(item) for item in line.split()]) for line in lines]).reshape(-1, 4)
        points = points[:, :3]
        n = points.shape[0]
        colors = np.tile(color, [n, 1])
    if not output_file.endswith('.ply'):
        output_file = output_file + '.ply'
    create_output(points, colors, output_file)


def bin2npy(input_file, output_file):
    with open(input_file, 'rb') as fp:
        points = np.fromfile(fp, dtype=np.float32).reshape([-1, 4])  # [n,4]
    if not output_file.endswith('.npy'):
        output_file = output_file + '.npy'
    np.save(output_file, points)


def bin2ply(input_file, output_file, color=None):
    if color is None:
        color = [0, 100, 100]
    with open(input_file, 'rb') as fp:
        points = np.fromfile(fp, dtype=np.float32).reshape([-1, 4])  # [n,4]
        points = points[:, :3]
        n = points.shape[0]
        colors = np.tile(color, [n, 1])
    if not output_file.endswith('.ply'):
        output_file = output_file + '.ply'
    create_output(points, colors, output_file)


def npy2ply(input_file, output_file, color=None):
    if color is None:
        color = [0, 100, 100]
    with open(input_file, 'rb') as fp:
        points = np.load(fp)
        # points = points.reshape([-1, 4])
        points = points[:, :3]
        n = points.shape[0]
        colors = np.tile(color, [n, 1])
    if not output_file.endswith('.ply'):
        output_file = output_file + '.ply'
    create_output(points, colors, output_file)


def npz2ply(input_file, output_point1, output_point2, output_flow, color=None, key=None):
    if color is None:
        color = [255, 0, 0]
    if key is None:
        key = {'pc1': 'pc1', 'pc2': 'pc2', 'flow': 'flow'}
    with open(input_file, 'rb') as fp:
        data = np.load(fp)
        pc1 = data[key['pc1']]
        pc2 = data[key['pc2']]
        flow = data[key['flow']]
        pc1 = pc1.astype('float32')
        pc2 = pc2.astype('float32')
        flow = flow.astype('float32')
        pc1 = pc1[:, :3]
        pc2 = pc2[:, :3]
        flow = flow[:, :3]
        n1 = pc1.shape[0]
        n2 = pc2.shape[0]
        colors1 = np.tile(color, [n1, 1])
        colors2 = np.tile(color, [n2, 1])
        if not output_point1.endswith('.ply'):
            output_point1 = output_point1 + '.ply'
        if not output_point2.endswith('.ply'):
            output_point2 = output_point2 + '.ply'
        if not output_flow.endswith('.npy'):
            output_flow = output_flow + '.npy'
        create_output(pc1, colors1, output_point1)
        create_output(pc2, colors2, output_point2)
        np.save(output_flow, flow)


def npz2plyTruth(input_file, output_point1, output_point2, output_point3, color=None):
    if color is None:
        color = [255, 0, 0]
    with open(input_file, 'rb') as fp:
        data = np.load(fp)
        for strkey in data.files:
            if 'pc1' in strkey:
                pc1 = data['pc1']
                pc2 = data['pc2']
                flow = data['flow']
                break
            if 'pos1' in strkey:
                pc1 = data['pos1']
                pc2 = data['pos2']
                flow = data['gt']
                break
        pc1 = pc1.astype('float32')
        pc2 = pc2.astype('float32')
        flow = flow.astype('float32')
        pc1 = pc1[:, :3]
        pc2 = pc2[:, :3]
        flow = flow[:, :3]
        n1 = pc1.shape[0]
        n2 = pc2.shape[0]
        colors1 = np.tile(color, [n1, 1])
        colors2 = np.tile(color, [n2, 1])
        flow = flow[:n1, :]
        truth = pc1 + flow
    if not output_point1.endswith('.ply'):
        output_point1 = output_point1 + '.ply'
    if not output_point2.endswith('.ply'):
        output_point2 = output_point2 + '.ply'
    if not output_point3.endswith('.ply'):
        output_point3 = output_point3 + '.ply'
    create_output(pc1, colors1, output_point1)
    create_output(pc2, colors2, output_point2)
    create_output(truth, colors1, output_point3)



def generate_ply_pc2(input_file, output_file):
    with open(input_file, 'rb') as fp:
        data = np.load(fp)
        pc = data['pc2']  # shape nx3
        # pc = data['pos2']  # shape nx3
        pc = np.reshape(pc, (-1, 3))
        n = pc.shape[0]
        color = np.tile([150, 220, 150], [n, 1])
        # color = data['color2']

        print('pc2.shape', pc.shape)

    create_output(pc, color, output_file)




def create_output(vertices, colors, filename):
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])
    np.savetxt(filename, vertices, fmt='%f %f %f %d %d %d')
    ply_header = '''ply
    		format ascii 1.0
    		element vertex %(vert_num)d
    		property float x
    		property float y
    		property float z
    		property uchar red
    		property uchar green
    		property uchar blue
    		end_header
    		\n
    		'''
    with open(filename, 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write(ply_header % dict(vert_num=len(vertices)))
        f.write(old)


