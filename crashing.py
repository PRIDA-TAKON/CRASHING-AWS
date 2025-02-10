# เตรียมเครื่องมือ
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
import PyPDF2
import gradio as gr


# ตรวจสอบว่าโฟลเดอร์ output ถูกสร้างขึ้นหรือไม่
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)


def MERG_PDF(pdf1=None, pdf2=None ,pdf3=None):
  pdf1File = open(pdf1, 'rb')
  pdf2File = open(pdf2, 'rb')
  pdf3File = open(pdf3, 'rb')

  pdf1Reader = PyPDF2.PdfReader(pdf1File)
  pdf2Reader = PyPDF2.PdfReader(pdf2File)
  pdf3Reader = PyPDF2.PdfReader(pdf3File)

  pdfWriter = PyPDF2.PdfWriter()

  for pageNum in range(len(pdf1Reader.pages)):
    pageObj = pdf1Reader.pages[pageNum]
    pdfWriter.add_page(pageObj)

  for pageNum in range(len(pdf2Reader.pages)):
    pageObj = pdf2Reader.pages[pageNum]
    pdfWriter.add_page(pageObj)

  for pageNum in range(len(pdf3Reader.pages)):
    pageObj = pdf3Reader.pages[pageNum]
    pdfWriter.add_page(pageObj)

  pdfOutputFile = open('merged_report.pdf', 'wb')
  pdfWriter.write(pdfOutputFile)
  pdfOutputFile.close()

  pdf1File.close()
  pdf2File.close()
  pdf3File.close()

def create_pdf_report(filename, df, image_path=None, header_text=None, critical_text =None, path_duration=None, result_text4=None):  # เพิ่ม header_text เป็น argument
  """สร้างรายงาน PDF จาก DataFrame"""
  doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
  elements = []



  # แปลงตัวเลขใน DataFrame เป็นจำนวนเต็ม
  for col in df.select_dtypes(include=['number']).columns:
    df[col] = df[col].map(lambda x: int(x) if not pd.isnull(x) else x)

  # Replace NaN values with blank strings
  df = df.fillna('')  # Replace all NaN values with ''

  # สร้างตารางจาก DataFrame
  data = [df.columns.tolist()] + df.values.tolist()
  table = Table(data, colWidths=[inch] * len(df.columns))

  # กำหนด Style ของตาราง
  style = TableStyle([
      ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
      ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
      ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
      ('GRID', (0, 0), (-1, -1), 1, colors.black),
      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
      ('BOX', (0, 0), (-1, -1), 1, colors.black),
      ('REPEATROWS', (0, 0), (0, 0)),
      ('FONTSIZE', (0, 0), (-1, -1), 7),
  ])
  table.setStyle(style)

  # เพิ่ม header text ถ้ามี
  if header_text:
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()
    header = Paragraph(header_text, styles['Heading1'])
    elements.append(header)

  # เพิ่มตารางลงใน elements
  elements.append(table)

    # เพิ่มข้อความใต้ตาราง
  from reportlab.lib.styles import getSampleStyleSheet
  styles = getSampleStyleSheet()

  critical_path_text = "Critical Path: " + str(critical_text)
  total_duration_text = "Total Duration: " + str(path_duration) + " days"
  over_head_text = "Indirect cost per day: " + str(result_text4) # Changed rusult_text4 to result_text4

  elements.append(Spacer(1, 0.2*inch))  # เพิ่มระยะห่าง
  elements.append(Paragraph(critical_path_text, styles['Normal']))
  elements.append(Paragraph(total_duration_text, styles['Normal']))
  elements.append(Paragraph(over_head_text, styles['Normal']))

  # เพิ่มรูปภาพ
  image = Image(image_path)
  image.drawHeight = 6 * inch
  image.drawWidth = 9 * inch
  elements.append(image)

  # สร้าง PDF
  doc.build(elements)

def create_pdf_report2(filename, df, header_text=None):  # เพิ่ม header_text เป็น argument
  """สร้างรายงาน PDF จาก DataFrame"""
  doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
  elements = []

  # แปลงตัวเลขใน DataFrame เป็นจำนวนเต็ม
  for col in df.select_dtypes(include=['number']).columns:
    df[col] = df[col].map(lambda x: int(x) if not pd.isnull(x) else x)

  # Replace NaN values with blank strings
  df = df.fillna('')  # Replace all NaN values with ''

  # สร้างตารางจาก DataFrame
  data = [df.columns.tolist()] + df.values.tolist()
  table = Table(data, colWidths=[inch] * len(df.columns))

  # กำหนด Style ของตาราง
  style = TableStyle([
      ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
      ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
      ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
      ('GRID', (0, 0), (-1, -1), 1, colors.black),
      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
      ('BOX', (0, 0), (-1, -1), 1, colors.black),
      ('REPEATROWS', (0, 0), (0, 0)),
      ('FONTSIZE', (0, 0), (-1, -1), 7),
  ])
  table.setStyle(style)

  # เพิ่ม header text ถ้ามี
  if header_text:
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()
    header = Paragraph(header_text, styles['Heading1'])
    elements.append(header)

  # เพิ่มตารางลงใน elements
  elements.append(table)

  # สร้าง PDF
  doc.build(elements)

# โหลดไฟล์ CSV ประกาศตัวแปร df และแสดงผล
def LOAD(file_path):
    global df
    df = pd.read_csv(file_path)
    print(df)

def CPM(dfa):
  global df
  try:
    # ตรวจสอบคอลัมน์ที่จำเป็น
    required_cols = ['Crash Cost', 'Normal Cost', 'Duration', 'Crash Duration']
    if not all(col in df.columns for col in required_cols):
      raise ValueError("CSV file is missing required columns.")
    # ตรวจสอบค่าในคอลัมน์
    if any(df['Duration'] == df['Crash Duration']):
      raise ValueError("Duration and Crash Duration cannot be equal.")
    # คำนวณ Crash Cost per Day
    df['Crash Cost per Day'] = (df['Crash Cost'] - df['Normal Cost']) / (df['Duration'] - df['Crash Duration'])
    # จัดเรียงข้อมูล
    df = df.sort_values(by="Crash Cost per Day")
    # แสดงผล
  except Exception as e:
    print(f"Error: {e}")

  G = nx.DiGraph()
  # เพิ่มโหนดพร้อมระยะเวลา (duration)
  for index, row in df.iterrows():
    activity = row['Activity']
    duration = row['Duration']
    G.add_node(activity, duration=duration)

  # เพิ่ม edge ตาม Predecessors พร้อมกำหนดน้ำหนัก (duration)
  for index, row in df.iterrows():
    activity = row['Activity']
    duration = row['Duration']  # ดึง duration ของกิจกรรม
    if pd.notna(row['Predecessors']):
        predecessors = row['Predecessors'].split()
        for predecessor in predecessors:
            G.add_edge(predecessor, activity, duration=duration)  # กำหนด duration เป็น weight

  # หา Critical Path
  if nx.is_directed_acyclic_graph(G):
    global critical_path
    critical_path = nx.dag_longest_path(G, weight='duration')  # ระบุ weight='duration'
    global critical_path_duration
    critical_path_duration = sum(G.nodes[node].get('duration', 0) for node in critical_path)
    global CPM_line
    CPM_line = " -> ".join(critical_path)
    print("Critical Path:", " -> ".join(critical_path))
    print("Total Duration:", critical_path_duration, "days")
  else:
    print("The graph is not a Directed Acyclic Graph (DAG).")
  #ระบุว่ากิจกรรมใดอยู่ใน CPM
  df['CPM'] = df['Activity'].apply(lambda x: 'YES' if x in critical_path else 'NO')
  df['Crash day'] = 0

  # สร้างคอลัมน์ 'Max_Possible_Crashing' ก่อน
  df['Max_Crashing'] = df['Duration'] - df['Crash Duration']

  global Max_Possible_Crashing
  Max_Possible_Crashing = df['Max_Crashing'].sum()

  global df_normal
  df_normal = df
  # แสดงผล
  print(df)

def CPM2(dfa):
  global df
  try:
    # ตรวจสอบคอลัมน์ที่จำเป็น
    required_cols = ['Crash Cost', 'Normal Cost', 'New crash duration', 'Crash Duration']
    if not all(col in df.columns for col in required_cols):
      raise ValueError("CSV file is missing required columns.")
    # ตรวจสอบค่าในคอลัมน์
    if any(df['Duration'] == df['Crash Duration']):
      raise ValueError("Duration and Crash Duration cannot be equal.")

    # แสดงผล
  except Exception as e:
    print(f"Error: {e}")

  G = nx.DiGraph()
  # เพิ่มโหนดพร้อมระยะเวลา (duration)
  for index, row in df.iterrows():
    activity = row['Activity']
    duration = row['New crash duration']
    G.add_node(activity, duration=duration)

  # เพิ่ม edge ตาม Predecessors พร้อมกำหนดน้ำหนัก (duration)
  for index, row in df.iterrows():
    activity = row['Activity']
    duration = row['New crash duration']  # ดึง duration ของกิจกรรม
    if pd.notna(row['Predecessors']):
        predecessors = row['Predecessors'].split()
        for predecessor in predecessors:
            G.add_edge(predecessor, activity, duration=duration)  # กำหนด duration เป็น weight

  # หา Critical Path
  if nx.is_directed_acyclic_graph(G):
    global critical_path
    critical_path = nx.dag_longest_path(G, weight='duration')  # ระบุ weight='duration'
    global critical_path_duration
    critical_path_duration = sum(G.nodes[node].get('duration', 0) for node in critical_path)

  else:
    print("The graph is not a Directed Acyclic Graph (DAG).")
  #ระบุว่ากิจกรรมใดอยู่ใน CPM
  df['CPM'] = df['Activity'].apply(lambda x: 'YES' if x in critical_path else 'NO')
  global CPM_line2
  CPM_line2 = " -> ".join(critical_path)

def DRAW(df):
    G = nx.DiGraph()
    # ระบุโหนด critical path และ START, END
    critical_nodes = set(critical_path)  # แปลงเป็น set เพื่อการค้นหาที่รวดเร็ว
    critical_nodes.update(['START', 'END'])  # เพิ่ม START, END
    labels = {}  # กำหนดค่า labels เป็น dictionary ว่างก่อน
    # กำหนดสีโหนด
    node_colors = ['red' if node in critical_nodes else 'lightblue' for node in G.nodes()]
    # เพิ่มโหนดพร้อมระยะเวลา (duration)
    for index, row in df.iterrows():
        activity = row['Activity']
        duration = row['Duration']
        G.add_node(activity, duration=duration)  # ไม่ต้องเพิ่ม LF, EF

    # เพิ่ม edge ตาม Predecessors พร้อมกำหนดน้ำหนัก (duration)
    for index, row in df.iterrows():
        activity = row['Activity']
        duration = row['Duration']
        if pd.notna(row['Predecessors']):
            predecessors = row['Predecessors'].split()
            for predecessor in predecessors:
                G.add_edge(predecessor, activity, duration=duration)
    # สร้าง dictionary dist
    distance = 10
    dist = {}
    for u in G.nodes():
        for v in G.nodes():
            if u != v:
                dist[(u, v)] = distance

    #หาลำดับชั้นของโหนด
    sorted_nodes = list(nx.algorithms.dag.topological_sort(G))
    # เพื่อจัดวางกราฟ
    pos = nx.kamada_kawai_layout(G, dist=dist, scale=5)# เพิ่ม scale เพื่อขยายกราฟ

    # ค้นหาตำแหน่ง X ที่เหมาะสม
    x_positions = [pos[node][0] for node in G.nodes() if node not in ('START', 'END')]
    avg_x = sum(x_positions) / len(x_positions) if x_positions else 0  # หากไม่มีโหนดอื่น ให้ x เป็น 0

    global node_positions  # อ้างอิงตัวแปร global
    node_positions = pos  # เก็บค่าตำแหน่งของโหนด

    # สีโหนด
    node_colors =  ['red' if node in critical_path or node == 'END' else 'lightblue' for node in G.nodes()]

    # วาดกราฟ
    fig, ax = plt.subplots(figsize=(18, 12))
    nx.draw_networkx_edges(G, pos, edge_color='black', width=1, arrowstyle='simple', arrowsize=20, min_source_margin=25, min_target_margin=25)
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, ax=ax)  # ใช้ node_color
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_weight="bold", font_color="black", font_size=20)  # เพิ่ม font_size (ปรับตามต้องการ)
    # แสดงชื่อโหนดและ Duration

    for node in G.nodes():
        if node in ('START', 'END'):  # ตรวจสอบว่าเป็น START หรือ END
            labels[node] = node  # กำหนด labels เป็นชื่อโหนดเฉยๆ
        elif 'duration' in G.nodes[node]:
            labels[node] = f"{node}\n({G.nodes[node]['duration']})"
        else:
            labels[node] = f"{node}\n(N/A)"


    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_weight="bold", font_color="black", font_size=20)

    ax.axis('off')

# สร้างกราฟที่ crashing แล้ว
def DRAW2(df):
    G = nx.DiGraph()
    # ระบุโหนด critical path และ START, END
    critical_nodes = set(critical_path)  # แปลงเป็น set เพื่อการค้นหาที่รวดเร็ว
    critical_nodes.update(['START', 'END'])  # เพิ่ม START, END
    labels = {}  # กำหนดค่า labels เป็น dictionary ว่างก่อน
    # กำหนดสีโหนด
    node_colors = ['red' if node in critical_nodes else 'lightblue' for node in G.nodes()]
    # เพิ่มโหนดพร้อมระยะเวลา (duration)
    for index, row in df.iterrows():
        activity = row['Activity']
        duration = row['New crash duration']
        G.add_node(activity, duration=duration)  # ไม่ต้องเพิ่ม LF, EF

    # เพิ่ม edge ตาม Predecessors พร้อมกำหนดน้ำหนัก (duration)
    for index, row in df.iterrows():
        activity = row['Activity']
        duration = row['New crash duration']
        if pd.notna(row['Predecessors']):
            predecessors = row['Predecessors'].split()
            for predecessor in predecessors:
                G.add_edge(predecessor, activity, duration=duration)

    # สร้าง dictionary dist
    distance = 10
    dist = {}
    for u in G.nodes():
        for v in G.nodes():
            if u != v:
                dist[(u, v)] = distance

    #หาลำดับชั้นของโหนด
    sorted_nodes = list(nx.algorithms.dag.topological_sort(G))
    # เพื่อจัดวางกราฟ
    pos = nx.kamada_kawai_layout(G, dist=dist, scale=5)# เพิ่ม scale เพื่อขยายกราฟ

    # ค้นหาตำแหน่ง X ที่เหมาะสม
     x_positions = [pos[node][0] for node in G.nodes() if node not in ('START', 'END')]
    avg_x = sum(x_positions) / len(x_positions) if x_positions else 0  # หากไม่มีโหนดอื่น ให้ x เป็น 0

    global node_positions  # อ้างอิงตัวแปร global
    node_positions = pos  # เก็บค่าตำแหน่งของโหนด

    # สีโหนด
    node_colors =  ['red' if node in critical_path or node == 'END' else 'lightblue' for node in G.nodes()]

    # วาดกราฟ
    fig, ax = plt.subplots(figsize=(18, 12))
    nx.draw_networkx_edges(G, pos, edge_color='black', width=1, arrowstyle='simple', arrowsize=20, min_source_margin=25, min_target_margin=25)
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, ax=ax)  # ใช้ node_color
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_weight="bold", font_color="black", font_size=20)  # เพิ่ม font_size (ปรับตามต้องการ)
    # แสดงชื่อโหนดและ Duration

    for node in G.nodes():
        if node in ('START', 'END'):  # ตรวจสอบว่าเป็น START หรือ END
            labels[node] = node  # กำหนด labels เป็นชื่อโหนดเฉยๆ
        elif 'duration' in G.nodes[node]:
            labels[node] = f"{node}\n({G.nodes[node]['duration']})"
        else:
            labels[node] = f"{node}\n(N/A)"


    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_weight="bold", font_color="black", font_size=20)

    ax.axis('off')

def DEMAND(dm):
  global Crash_time
  Crash_time = dm

def OVERHEAD(dm):
  global Over_Head
  Over_Head = dm
  print('Over Head',dm,'per day')

def DECREASE_CPM2(dfa,Crash_time):
    global df, critical_path_duration, crashing_round, df_best_option  # เพิ่ม df_best_option
    min_total_cost = float('inf')  # กำหนดค่าเริ่มต้นให้สูงที่สุด
    df_best_option = None  # กำหนดค่าเริ่มต้นเป็น None

    while True:
        # 1. สร้าง cpm_yes โดยกรอง df เอาเฉพาะรายการที่มี CPM เป็น YES และ New crash duration > Crash Duration
        df['Max_Crashing'] = df['Duration'] - df['Crash Duration']
        df['New crash duration'] = df['Duration'] - df['Crash day']
        cpm_yes = df[(df['CPM'] == 'YES') & (df['New crash duration'] > df['Crash Duration'])]

        # ตรวจสอบว่ายังมี CPM ที่เป็น YES เหลืออยู่หรือไม่
        if cpm_yes.empty:
            break  # หยุดลูปถ้าไม่มี CPM ที่เป็น YES แล้ว

        # 2. df['New crash duration'] = df['Duration'] - df['Crash day']
        df['New crash duration'] = df['Duration'] - df['Crash day']

        # 3. หา index ของแถวที่มี Crash Cost per Day ต่ำสุดใน cpm_yes
        min_cost_index = cpm_yes['Crash Cost per Day'].idxmin()

        # 4. เพิ่มค่า Crash day ขึ้น 1 ในแถวที่เลือก
        df.loc[min_cost_index, 'Crash day'] += 1

        # 5. ใช้งานฟังชั่น CPM2 เพื่อหาค่า critical_path_duration ของ df
        CPM2(df)
        df['New crash duration'] = df['Duration'] - df['Crash day']
        df['Cost'] = (df['Crash day'] * df['Crash Cost per Day']) + df['Normal Cost']+Over_Head*df['New crash duration' ]

        CPM2(df)
        Direct_cost =  df['Normal Cost'].sum(skipna=True)+((df['Crash day']*df['Crash Cost per Day']).sum(skipna=True))
        Indirect_cost = int(critical_path_duration)*int(Over_Head)
        add_crashing_row(
          crashing_round,
          CPM_line2, critical_path_duration,
          Direct_cost,
          Indirect_cost,
          Direct_cost + Indirect_cost
          )
        # ตรวจสอบและอัพเดตค่า min_total_cost และ df_best_option
        if crashing_round.iloc[-1]['Total'] < min_total_cost:
            min_total_cost = crashing_round.iloc[-1]['Total']
            df_best_option = df.copy()  # คัดลอก df เพื่อเก็บค่าที่ดีที่สุด


    # ส่ง crashing_round ออกมา
    return crashing_round
    return df_best_option # ส่งค่า df_best_option ออกมา
    return df

def MAKE_CRASH_TABLLE(dfa):
  # สร้างตาราง crashing_round ว่าง
  global crashing_round
  crashing_round = pd.DataFrame(columns=['Crashing', 'Critical Path','Days', 'Direct cost', 'Indirect cost', 'Total'])
  # เพิ่มข้อมูลแถวแรก
  global Direct_cost
  global Indirect_cost
  Direct_cost =  df['Normal Cost'].sum(skipna=True)
  Indirect_cost = critical_path_duration*Over_Head
  crashing_round.loc[0] = [
    'Before Crashing',
    CPM_line,
    critical_path_duration,
    Direct_cost,
    Indirect_cost,
    Direct_cost + Indirect_cost]

# ฟังก์ชันสำหรับเพิ่มแถวใหม่
def add_crashing_row(crashing_round, critical_path, days, direct_cost, indirect_cost, total_cost):
  # หาจำนวนแถวปัจจุบัน
  num_rows = len(crashing_round)

  # สร้างชื่อ Crashing สำหรับแถวใหม่
  crashing_name = f"Crashing {num_rows}"

  # เพิ่มแถวใหม่
  crashing_round.loc[num_rows] = [crashing_name, critical_path, days, direct_cost, indirect_cost, total_cost]

  return crashing_round

# แสดงตาราง
  display(crashing_round)

# สร้าง UI กำลังพัฒนา
def run_program(csv_file, indirect_cost):
  """ฟังก์ชันที่ใช้ประมวลผลข้อมูลจาก UI"""
  # โหลดไฟล์ CSV
  df = pd.read_csv(csv_file.name)

  # กำหนดค่า indirect cost
  OVERHEAD(indirect_cost)

  # ... (โค้ดเดิมของคุณ) ...
  LOAD(csv_file.name) # โหลดไฟล์


  CPM(df) # เตรียมไฟล์ หา คริติคอลพาท
  df['Max_Crashing'] = df['Duration'] - df['Crash Duration']
  MAKE_CRASH_TABLLE(df) # สร้างตารางแรก

  #สร้างไดอะแกรม
  plt.figure(figsize=(10, 6))  # กำหนดขนาดรูปภาพ (ปรับตามต้องการ)
  DRAW(df) # เรียกใช้ฟังก์ชัน DRAW
  plt.savefig('output/CPM_graph.png')  # บันทึกรูปภาพ DRAW
  
  # เรียกใช้ฟังก์ชัน create_pdf_report
  create_pdf_report("output/CPM_report.pdf"
  , df
  , image_path= os.path.join("output","CPM_graph.png")
  , header_text="DATA FOR CRASHING"
  , critical_text= CPM_line
  , path_duration= critical_path_duration
  , result_text4= Over_Head)

  #เริ่ม crashing
  limit_crash_time = df['Max_Crashing'].sum(skipna=True)
  DECREASE_CPM2(df,limit_crash_time)
  # crashing เสร็จ
  print(crashing_round)
  print(df_best_option)  # ใช้ df_best_option
  CPM2(df_best_option)
  #สร้างกราฟ
  plt.figure(figsize=(10, 6))  # กำหนดขนาดรูปภาพ (ปรับตามต้องการ)
  DRAW2(df_best_option) # เรียกใช้ฟังก์ชัน DRAW2
  plt.savefig('output/CPM_graph_crashed.png')  # บันทึกรูปภาพ DRAW2
  
  #  สร้างไฟล์ CSV จากตัวแปร df_best_option และ crashing_round
  df_best_option.to_csv('Best_option_result.csv', index=False)
  crashing_round.to_csv('CRASH_TABLLE.csv', index=False)

  # เรียกใช้ฟังก์ชัน create_pdf_report
  create_pdf_report("output/Best_option_report.pdf"
  , df_best_option
  , image_path= os.path.join("output","CPM_graph_crashed.png")
  , critical_text= CPM_line2
  , header_text="RESUIL FROM CRASHING"
  , path_duration= (df_best_option[df_best_option['CPM'] == 'YES'])['New crash duration'].sum()
  , result_text4= Over_Head)

  create_pdf_report2("output/Crash_table.pdf",crashing_round, header_text= "CRASH TABLE")

  # สร้างพาธไฟล์ PDF
  pdf1 = os.path.join("output", "CPM_report.pdf")
  pdf2 = os.path.join("output", "Crash_table.pdf")
  pdf3 = os.path.join("output", "Best_option_report.pdf")

  # เรียกใช้ฟังก์ชัน MERG_PDF ด้วยพาธใหม่
  MERG_PDF(pdf1=pdf1, pdf2=pdf2, pdf3=pdf3)

  return 'merged_report.pdf'  # return พาธของไฟล์ PDF

# สร้าง UI
iface = gr.Interface(
    fn=run_program,
    inputs=[
        gr.File(label="UPLOAD .CSV"),
        gr.Number(label="INDIRECT COST PER DAY", precision=0),
    ],
    outputs=gr.File(),  # ใช้ gr.File() เพื่อแสดงผลไฟล์
    title="PROJECT CRASHING",
    description="Upload your CSV file and get a crashing report.",
)

# แสดง UI
iface.launch(server_name="0.0.0.0", server_port=8080,debug=True)
# เพิ่มการตรวจสอบว่าแอพกำลังรันอยู่
if __name__ == "__main__":
    print("Application is running")
    # เรียกใช้ฟังก์ชันหรือโค้ดที่ต้องการรัน
