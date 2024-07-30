def billing_app_page():
    global song, cap, c_bill_txt, cphn_txt, addproduct_e, cname_txt, discount_txt, total_bill_txt, addquantity_e, capp, cap, mstr_df_prd, cam1, cam2, sac4_e, sac3_e, sac2_e, sac1_e, cur, mycon, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all
    db_conn_funct()
    quant_list_bill = pd.DataFrame()
    total_list_bill = pd.DataFrame()

    mstr_df_prd = pd.DataFrame({'pname': [], 'mrp': [], 'barcode': [], 'pid': [
    ], 'quantity': [], 'total': [], 'profit': [], 'total_profit': []})

    bc_list_bill_all = []
    name_list_bill = pd.DataFrame()
    pid_list_bill = pd.DataFrame()
    mrp_list_bill = pd.DataFrame()
    bc_list_bill = pd.DataFrame()

    cam1 = True

    if cam2:
        cam2 = False
        capp.release()

    F1 = LabelFrame(billing_frame, fg=us_fg, bg=us_bg)
    F1.place(x=0, y=0, relwidth=1)
    fc1 = LabelFrame(F1, fg=us_fg, bg=us_bg, borderwidth=0, relief="raised")
    fc1.grid(row=0, column=0, padx=40, pady=3)

    fc2 = LabelFrame(F1, fg=us_fg, bg=us_bg, relief="raised", borderwidth=0)
    fc2.grid(row=0, column=1, padx=37, pady=3)

    fc3 = LabelFrame(F1, fg=us_fg, bg=us_bg, relief="raised")
    fc3.grid(row=0, column=2, padx=40, pady=3)

    cname_lbl = Label(fc1, text="Customer Name:",
                      bg=us_bg, borderwidth=0, fg=us_fg, font=('Helvetica', 15, 'bold'))
    cname_lbl.grid(row=0, column=0, padx=10)
    cname_txt = Entry(fc1, width=15, font='arial 15')
    cname_txt.grid(row=0, column=1, padx=10)

    cphn_lbl = Label(fc2, text="Email:", bg=us_bg, fg=us_fg,
                     font=('Helvetica', 15, 'bold'), borderwidth=0)
    cphn_lbl.grid(row=0, column=2, padx=10)
    cphn_txt = Entry(fc2, width=23, font='arial 15')
    cphn_txt.grid(row=0, column=3, padx=10)

    c_bill_lbl = Label(fc3, text="Bill Number:", bg=us_bg, fg=us_fg,
                       font=('Helvetica', 15, 'bold'))
    c_bill_lbl.grid(row=0, column=4, padx=10)
    c_bill_txt = Entry(fc3, width=15, font=(
        'Helvetica', 15, 'bold'), state='disable')
    c_bill_txt.grid(row=0, column=5, padx=10)

    # ******************************************************************************

    # middle window - barcode and item details

    F2 = LabelFrame(billing_frame, fg=mid_fg, bg=mid_bg)
    F2.place(x=0, y=43, relwidth=1)

    barcode = LabelFrame(F2, fg=us_fg, bg=us_bg)
    barcode.grid(row=0, column=0, padx=5, pady=3)

    items = LabelFrame(F2, fg=mid_fg, bg=mid_bg, height=500)
    items.grid(row=0, column=1, padx=20, pady=3)

    # labels
    barcode_lbl = Label(barcode, text="Barcode", bg=us_bg, font=(
        'Helvetica', 15, 'bold'), width=50, height=20)
    barcode_lbl.grid(row=0, column=0, padx=10)

    lmain = Label(barcode_lbl)
    lmain.grid(row=0, column=0, padx=30, pady=50)

# ============================= bill id gen ======================================
    bill_qry = "select `bill_id` from bill_details;"
    bill_list_df = pd.read_sql(bill_qry, mycon)
    bill_list_all = bill_list_df['bill_id'].tolist()
    import string
    import random
    bill_id_new = ''.join(random.choices(
        string.ascii_letters + string.digits, k=8))
    while bill_id_new in bill_list_all:
        bill_id_new = ''.join(random.choices(
            string.ascii_letters + string.digits, k=8))

    c_bill_txt.configure(state='normal')
    if len(c_bill_txt.get()) > 0:
        c_bill_txt.delete(0, END)

    c_bill_txt.insert(0, bill_id_new)
    c_bill_txt.configure(state='disable')
    # print(bill_id_new)

# ===================================================================

    cap = cv2.VideoCapture(0)

    manual_mode = LabelFrame(items, fg=us_fg, bg=us_bg)
    manual_mode.grid(row=0, column=0, padx=0, pady=11)

    items_bill_live = LabelFrame(items, fg=mid_fg, bg=mid_bg)
    items_bill_live.grid(row=1, column=0, padx=25, pady=3)

    Label(manual_mode, text="PRODUCT ID", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    addproduct_e = Entry(manual_mode, width=15, font='arial 15')
    addproduct_e.grid(row=1, column=0, padx=5, pady=8)

    Label(manual_mode, text="QUANTITY", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=1)
    addquantity_e = Entry(manual_mode, width=15, font='arial 15')
    addquantity_e.grid(row=1, column=1, padx=5, pady=8)

    details = LabelFrame(items_bill_live, fg=mid_fg, bg=mid_bg, height=510)
    details.grid(row=1, column=0)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    name_detail.grid(row=0, column=0)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    cost_detail.grid(row=0, column=3)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    mrp_detail.grid(row=0, column=1)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    quant_detail.grid(row=0, column=2)

    def mult_view(*args):
        sac4_e.yview(*args)
        sac3_e.yview(*args)
        sac2_e.yview(*args)
        sac1_e.yview(*args)

    vsb = Scrollbar(details)
    vsb.grid(row=0, column=4, sticky='ns')
    vsb.configure(command=mult_view)

    Label(name_detail, text="NAME", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac1_e = Text(name_detail, width=18, height=15, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac1_e.grid(row=1, column=0)

    Label(quant_detail, text="QUANTITY", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac2_e = Text(quant_detail, width=13, height=15,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac2_e.grid(row=1, column=0)

    Label(mrp_detail, text="MRP", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac3_e = Text(mrp_detail, width=15, height=15, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac3_e.grid(row=1, column=0)

    Label(cost_detail, text="TOTAL", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac4_e = Text(cost_detail, width=15, height=15, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac4_e.grid(row=1, column=0)

    # bottom window - bill details and action buttons

    F3 = LabelFrame(billing_frame, fg=us_fg, bg=us_bg, relief="raised")
    F3.place(x=0, y=558, relwidth=1)
    discount = LabelFrame(F3, fg=us_fg, bg=us_bg, relief="raised")
    discount.grid(row=0, column=0, padx=40, pady=3)

    total_bill = LabelFrame(F3, fg=us_fg, bg=us_bg, relief="raised")
    total_bill.grid(row=0, column=1, padx=37, pady=3)

    generate_btn = LabelFrame(F3, fg=us_fg, bg=us_bg,  borderwidth='0')
    generate_btn.grid(row=0, column=4, padx=40, pady=3)

    total_btn = LabelFrame(F3, fg=us_fg, bg=us_bg, borderwidth='0')
    total_btn.grid(row=0, column=3, padx=40, pady=3)

    discount_lbl = Label(discount, text="Discount",
                         bg=us_bg, fg=us_fg, font=('Helvetica', 15, 'bold'))
    discount_lbl.grid(row=0, column=0, padx=10)
    discount_txt = Entry(discount, width=15, font='arial 15')
    discount_txt.grid(row=1, column=0, padx=10)

    discount_txt.insert(0, int(0))

    total_bill_lbl = Label(total_bill, text="Total Amount",
                           bg=us_bg, fg=us_fg, font=('Helvetica', 15, 'bold'))
    total_bill_lbl.grid(row=0, column=0, padx=10)

    total_bill_txt = Entry(total_bill, width=15,
                           font='arial 15', state='disable')
    total_bill_txt.grid(row=1, column=0, padx=10)

    global barcode_all_list
    barcode_qry = "select `barcode` from product;"
    barcode_all_df = pd.read_sql(barcode_qry, mycon)
    barcode_all_list = barcode_all_df['barcode'].tolist()

    global cnt123

    cnt123 = False

    def asd123():
        global cnt123
        cnt123 = True
        messagebox.showinfo("PRODUCT NOT AVAILABLE", "Pls add the product to inventory first !")
        cnt123 = False

    def show_frame():
        _, img = cap.read()
        img = cv2.resize(img, (400, 350))
        frame = img
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        hhh = ii.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=hhh)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

        for barcode in decode(img):
            global mycon, song, master_barcode_list, cur, barcode_all_df, bill_id_new, mstr_df_prd, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all

            myData = barcode.data.decode('utf-8')

            if myData in barcode_all_list:

                one_row_qry = "select `pname`, `mrp`, `barcode`, `pid`,`profit`, `quantity` as 'quant_main' from product where `barcode` = %s;" % (
                    myData,)
                temp_df_pro = pd.read_sql(one_row_qry, mycon)
                temp_df_pro['quantity'] = [int(1)]
                total_new = int(temp_df_pro['mrp'].to_string(index=False))
                temp_df_pro['total'] = [total_new]

                total_profit_new = int(
                    temp_df_pro['profit'].to_string(index=False))
                temp_df_pro['total_profit'] = [total_profit_new]

                master_barcode_list = mstr_df_prd['barcode'].tolist()
                ind_main = mstr_df_prd[mstr_df_prd['barcode']
                                       == myData].index.values
                if myData not in master_barcode_list:
                    q_new_temp = 1
                else:
                    q_new_temp = int(
                        float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False))) + 1

                pid_qry_bill = "select `barcode` , `quantity` as 'quant_main' from product;"
                pid_qry_bill_df = pd.read_sql(pid_qry_bill, mycon)
                pid_qry_bill_list = pid_qry_bill_df['barcode'].tolist()
                quant_ind = pid_qry_bill_list.index(myData)

                if myData in master_barcode_list:
                    if int(float(pid_qry_bill_df['quant_main'].iloc[quant_ind])) - q_new_temp >= 0:
                        pygame.mixer.init()
                        pygame.mixer.music.load("scanner_sound.mp3")
                        pygame.mixer.music.play()
                        ind_main = mstr_df_prd[mstr_df_prd['barcode']
                                               == myData].index.values
                        q_new_temp = int(
                            float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False))) + 1
                        mstr_df_prd.loc[ind_main, 'quantity'] = q_new_temp
                        total_new = int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(
                            index=False)))*(int(float(mstr_df_prd['mrp'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total'] = [total_new]

                        total_new = int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(
                            index=False))) * (int(float(mstr_df_prd['profit'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total_profit'] = [total_new]
                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")

                else:
                    if int(float(temp_df_pro['quant_main'].to_string(index=False))) > 0:
                        pygame.mixer.init()
                        pygame.mixer.music.load("scanner_sound.mp3")
                        pygame.mixer.music.play()
                        mstr_df_prd = mstr_df_prd.append(
                            temp_df_pro, ignore_index=True)

                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")

            else:
                if cnt123 == False:
                    asd123()

            time.sleep(1.2)

    def add_product_tobill():
        global mycon, cur, barcode_all_df, master_barcode_list, bill_id_new, mstr_df_prd, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all, addproduct_e, addquantity_e
        pid_qry_bill = "select `pid`, `quantity` as 'quant_main' from product;"
        pid_qry_bill_df = pd.read_sql(pid_qry_bill, mycon)
        pid_qry_bill_list = pid_qry_bill_df['pid'].tolist()

        if len(addproduct_e.get()) > 0 and len(addquantity_e.get()) > 0:
            if (addproduct_e.get()) in pid_qry_bill_list and int(addquantity_e.get()) > 0:
                if addproduct_e.get() in (mstr_df_prd['pid'].tolist()):
                    ind_main = mstr_df_prd[mstr_df_prd['pid']
                                           == addproduct_e.get()].index.values
                    q_new = int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(
                        index=False))) + int(addquantity_e.get())

                    quant_ind = pid_qry_bill_list.index(
                        str(addproduct_e.get()))

                    if int(float(pid_qry_bill_df['quant_main'].iloc[quant_ind])) - q_new >= 0:

                        mstr_df_prd.loc[ind_main, 'quantity'] = q_new
                        total_new = q_new * \
                            (int(
                                float(mstr_df_prd['mrp'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total'] = [total_new]
                        total_new = q_new * \
                            (int(
                                float(mstr_df_prd['profit'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total_profit'] = [total_new]

                        sac1_e.configure(state="normal")

                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')

                        addproduct_e.delete(0, END)
                        addquantity_e.delete(0, END)
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")

                else:

                    quant_ind = pid_qry_bill_list.index(
                        str(addproduct_e.get()))
                    if int(float(pid_qry_bill_df['quant_main'].iloc[quant_ind])) - int(addquantity_e.get()) >= 0:
                        one_row_qry = "select `pname`, `mrp`, `barcode`, `pid`,`profit`, `quantity` as 'quant_main' from product where `pid` = '%s';" % (
                            addproduct_e.get(),)
                        temp_df_pro = pd.read_sql(one_row_qry, mycon)
                        temp_df_pro['quantity'] = [int(addquantity_e.get())]
                        if int(float(temp_df_pro['quant_main'].to_string(index=False))) > 0:
                            total_new = int(temp_df_pro['mrp'].to_string(
                                index=False)) * int(addquantity_e.get())
                            temp_df_pro['total'] = [total_new]

                            total_new = int(temp_df_pro['profit'].to_string(
                                index=False)) * int(addquantity_e.get())
                            temp_df_pro['total_profit'] = [total_new]

                            mstr_df_prd = mstr_df_prd.append(
                                temp_df_pro, ignore_index=True)

                            sac1_e.configure(state="normal")
                            sac1_e.delete('1.0', END)
                            sac1_e.insert(
                                '1.0', mstr_df_prd['pname'].to_string(index=False))
                            sac1_e.configure(state="disable")

                            sac2_e.configure(state="normal")
                            sac2_e.delete('1.0', END)
                            sac2_e.insert(
                                '1.0', mstr_df_prd['quantity'].to_string(index=False))
                            sac2_e.configure(state='disable')

                            sac3_e.configure(state="normal")
                            sac3_e.delete('1.0', END)
                            sac3_e.insert(
                                '1.0', mstr_df_prd['mrp'].to_string(index=False))
                            sac3_e.configure(state="disable")

                            sac4_e.configure(state="normal")
                            sac4_e.delete('1.0', END)
                            sac4_e.insert(
                                '1.0', mstr_df_prd['total'].to_string(index=False))
                            sac4_e.configure(state='disable')

                            addproduct_e.delete(0, END)
                            addquantity_e.delete(0, END)
                        else:
                            messagebox.showinfo(
                                "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is not enough")

            else:
                messagebox.showinfo(
                    "PRODUCT NOT FOUND", "The product with pid "+addproduct_e.get()+" not found !")
                addproduct_e.delete(0, END)
                addquantity_e.delete(0, END)
        else:
            messagebox.showinfo("INVALID INPUT", "Fill all details first !")

    def remove_item_frombill():
        global mycon, cur, barcode_all_df, master_barcode_list, bill_id_new, mstr_df_prd, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all, addproduct_e, addquantity_e
        if len(addquantity_e.get()) > 0 and len(addproduct_e.get()) > 0:
            if addproduct_e.get() in mstr_df_prd['pid'].tolist():
                ind_main = mstr_df_prd[mstr_df_prd['pid']
                                       == addproduct_e.get()].index.values
                q_now_ibbill = int(
                    float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False)))
                if q_now_ibbill - int(addquantity_e.get()) >= 0:

                    q_new = q_now_ibbill - int(addquantity_e.get())
                    mstr_df_prd.loc[ind_main, 'quantity'] = [q_new]
                    total_new = q_new * \
                        (int(
                            float(mstr_df_prd['mrp'].iloc[ind_main].to_string(index=False))))
                    mstr_df_prd.loc[ind_main, 'total'] = [total_new]

                    total_new = q_new * \
                        (int(
                            float(mstr_df_prd['profit'].iloc[ind_main].to_string(index=False))))
                    mstr_df_prd.loc[ind_main, 'total_profit'] = [total_new]

                    sac1_e.configure(state="normal")
                    sac1_e.delete('1.0', END)
                    sac1_e.insert(
                        '1.0', mstr_df_prd['pname'].to_string(index=False))
                    sac1_e.configure(state="disable")

                    sac2_e.configure(state="normal")
                    sac2_e.delete('1.0', END)
                    sac2_e.insert(
                        '1.0', mstr_df_prd['quantity'].to_string(index=False))
                    sac2_e.configure(state='disable')

                    sac3_e.configure(state="normal")
                    sac3_e.delete('1.0', END)
                    sac3_e.insert(
                        '1.0', mstr_df_prd['mrp'].to_string(index=False))
                    sac3_e.configure(state="disable")

                    sac4_e.configure(state="normal")
                    sac4_e.delete('1.0', END)
                    sac4_e.insert(
                        '1.0', mstr_df_prd['total'].to_string(index=False))
                    sac4_e.configure(state='disable')

                    addproduct_e.delete(0, END)
                    addquantity_e.delete(0, END)

                    if int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False))) == 0:

                        mstr_df_prd = mstr_df_prd.drop(
                            mstr_df_prd.index[ind_main])
                        mstr_df_prd.reset_index(drop=True, inplace=True)

                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')
                    else:
                        pass

                    if mstr_df_prd.empty:
                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)

                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)

                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)

                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)

                        sac4_e.configure(state='disable')

                else:
                    messagebox.showinfo("NOT ENOUGH ITEMS",
                                        "Not enough items to remove !")
                    addproduct_e.delete(0, END)
                    addquantity_e.delete(0, END)
            else:
                messagebox.showinfo(
                    "INVALID INPUT", "No such product found in order list !")
                addproduct_e.delete(0, END)
                addquantity_e.delete(0, END)
        else:
            messagebox.showinfo("INVALID INPUT", "Fill all details first !")

    def total_amt_bill_gen():
        global mstr_df_prd, total_bill_txt,  discount_txt
        total_amt_display = mstr_df_prd['total'].sum()
        total_bill_txt.configure(state='normal')
        if len(total_bill_txt.get()) > 0:
            total_bill_txt.delete(0, END)
        if len(discount_txt.get()) > 0:
            if int(discount_txt.get()) <= 100:
                percent_dis = int(discount_txt.get())*0.01
                total_amt_display = round(total_amt_display*(1 - percent_dis))

            else:
                messagebox.showinfo(
                    "INVALID INPUT", "Discount must be atmost 100")

        else:
            messagebox.showinfo(
                "INVALID INPUT", "Fill both tax and discount first !")

        total_bill_txt.insert(0, total_amt_display)
        total_bill_txt.configure(state='disable')

    def generate_bill_main():
        global mycon, sac1_e, sac2_e, sac3_e, sac4_e, cap, c_bill_txt, cphn_txt, addproduct_e, discount_txt, cname_txt, cur, barcode_all_df, master_barcode_list, bill_id_new, mstr_df_prd, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all, addproduct_e, addquantity_e, total_bill_txt, barcode_all_list
        is_df_notnull = bool(1 ^ int(mstr_df_prd.empty))
        if is_df_notnull and len(cname_txt.get()) > 0 and len(discount_txt.get()) > 0:
            generate_btn_lbl.configure(state='disable')
            # ======== total bill ========================

            total_amt_display = mstr_df_prd['total'].sum()
            total_bill_txt.configure(state='normal')

            if len(total_bill_txt.get()) > 0:
                total_bill_txt.delete(0, END)
            if len(discount_txt.get()) > 0:
                if int(discount_txt.get()) <= 100:
                    percent_dis = int(discount_txt.get()) * 0.01
                    total_amt_display = round(
                        total_amt_display * (1 - percent_dis))

                else:
                    messagebox.showinfo(
                        "INVALID INPUT", "Discount must be atmost 100")

            else:
                messagebox.showinfo(
                    "INVALID INPUT", "Fill both tax and discount first !")

            total_bill_txt.insert(0, total_amt_display)

            total_bill_txt.configure(state='disable')

        # ==========================================================================
            pname_list = mstr_df_prd['pname'].tolist()
            quantity_list = mstr_df_prd['quantity'].tolist()
            proxquant_list1 = mstr_df_prd['total_profit'].tolist()
            bc_list = mstr_df_prd['barcode'].tolist()
            mrpxquant1 = mstr_df_prd['total'].tolist()
            items_count_all = mstr_df_prd['quantity'].sum()
            pid_list_all = mstr_df_prd['pid'].tolist()
            proxquant_list = []
            mrpxquant = []
            for asd in range(mstr_df_prd.shape[0]):

                mrp_new = int(mrpxquant1[asd])*(int(discount_txt.get())/100)
                mrp_main = int(mrpxquant1[asd]) * \
                    (100 - int(discount_txt.get()))//100
                p_new = proxquant_list1[asd] - mrp_new
                proxquant_list.append(p_new)
                mrpxquant.append(mrp_main)

            total_profit_bill = sum(proxquant_list)
            qry_asd = "select * from stats;"
            stats_now = pd.read_sql(qry_asd, mycon)

            qry_asd = "select `quantity`, `sold`, `pid` from product;"
            product_now = pd.read_sql(qry_asd, mycon)

            num_of_rows = mstr_df_prd.shape[0]

            date_now = date.today()

            if len(cphn_txt.get()) == 0:

                qry3 = "INSERT INTO `bill_details` (`bill_id`, `items`, `bill_price`, `bill_profit`, `bill_date`, `c_name`, `c_email`, `discount`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', NULL, '%s');" % (
                    bill_id_new, items_count_all, total_amt_display, total_profit_bill, date_now, cname_txt.get(),
                    discount_txt.get(),)
            else:
                qry3 = "INSERT INTO `bill_details` (`bill_id`, `items`, `bill_price`, `bill_profit`, `bill_date`, `c_name`, `c_email`, `discount`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                    bill_id_new, items_count_all, total_amt_display, total_profit_bill, date_now, cname_txt.get(),
                    cphn_txt.get(), discount_txt.get(),)

            cur.execute(qry3)
            mycon.commit()

            for jj in range(num_of_rows):
                qry1 = "INSERT INTO `sales` (`bill_id`, `pname`, `quantity`, `profit_pp`, `barcode`) VALUES ('%s', '%s', '%s', '%s', '%s');" % (
                    bill_id_new, pname_list[jj], quantity_list[jj], proxquant_list[jj], bc_list[jj],)
                cur.execute(qry1)
                mycon.commit()

                if pname_list[jj] in stats_now['pname'].tolist():
                    ind_main = stats_now[stats_now['pname']
                                         == pname_list[jj]].index.values
                    sold_new = int(float(stats_now['sold'].iloc[ind_main].to_string(
                        index=False))) + int(quantity_list[jj])
                    net_rev_new = int(float(stats_now['net_revenue'].iloc[ind_main].to_string(
                        index=False))) + int(mrpxquant[jj])
                    net_pro_new = int(float(stats_now['net_profit'].iloc[ind_main].to_string(
                        index=False))) + int(proxquant_list[jj])

                    qry2 = "UPDATE `stats` SET `sold`='%s',`net_revenue`='%s',`net_profit`='%s' WHERE `pname` = '%s';" % (
                        sold_new, net_rev_new, net_pro_new, pname_list[jj],)
                else:
                    qry2 = "INSERT INTO `stats` (`pname`, `sold`, `net_revenue`, `net_profit`) VALUES ('%s', '%s', '%s', '%s')" % (
                        pname_list[jj], quantity_list[jj], mrpxquant[jj], proxquant_list[jj],)

                cur.execute(qry2)
                mycon.commit()

                ind_main = product_now[product_now['pid']
                                       == pid_list_all[jj]].index.values
                quant_new = int(float(product_now['quantity'].iloc[ind_main].to_string(
                    index=False))) - quantity_list[jj]

                sold_new = int(float(product_now['sold'].iloc[ind_main].to_string(
                    index=False))) + quantity_list[jj]

                qry4 = "UPDATE `product` SET `quantity`='%s',`sold`='%s' WHERE `pid` = '%s';" % (
                    quant_new, sold_new, pid_list_all[jj])
                cur.execute(qry4)
                mycon.commit()

            quant_list_bill = pd.DataFrame()
            total_list_bill = pd.DataFrame()
            try:
                billdf_pdf = mstr_df_prd[[
                    'pname', 'mrp', 'quantity', 'total'].copy()]

                if mstr_df_prd.shape[0] == 1:
                    billdf_pdf['DISCOUNT'] = str(discount_txt.get()) + "%"
                    billdf_pdf['total_all'] = "₹" + str(total_amt_display)
                    billdf_pdf['Bill Id'] = bill_id_new

                else:

                    dt_temp = ['~' for jj in range(mstr_df_prd.shape[0] - 1)]
                    dt_temp2 = ['~' for jj in range(mstr_df_prd.shape[0] - 1)]
                    dt_temp3 = ['~' for jj in range(mstr_df_prd.shape[0] - 1)]

                    dd_tmp = 'discount : ' + str(discount_txt.get()) + "%"
                    tt_tmp = 'total : ₹' + str(total_amt_display)
                    bd_tmp = 'bill id : ' + str(bill_id_new)
                    dt_temp.append(tt_tmp)
                    dt_temp2.append(bd_tmp)
                    dt_temp3.append(dd_tmp)

                    billdf_pdf['DISCOUNT'] = dt_temp3
                    billdf_pdf['total_all'] = dt_temp
                    billdf_pdf['Bill ID'] = dt_temp2

                billdf_pdf.index += 1

                billdf_pdf = billdf_pdf.rename(
                    {'pname': 'ITEM NAME', 'mrp': 'RATE', 'total': 'VALUE', 'total_all': 'BILL TOTAL'}, axis=1)
                billdf_pdf['VALUE_sub'] = billdf_pdf['VALUE'] * \
                    (int(discount_txt.get())*0.01)
                billdf_pdf['VALUE'] -= billdf_pdf['VALUE_sub']
                billdf_pdf = billdf_pdf.drop('VALUE_sub', 1)

                fig, ax = plt.subplots(figsize=(12, 4))
                ax.axis('tight')
                ax.axis('off')
                the_table = ax.table(
                    cellText=billdf_pdf.values, colLabels=billdf_pdf.columns, loc='top')

                pp = PdfPages("foo.pdf")

                pp.savefig(fig, bbox_inches='tight')

                pp.close()

                # ========== email ===================

                EMAIL_ADDRESS = 'YOUR EMAIL GOES HERE'
                EMAIL_PASSWORD = 'YOUR PASSWORD GOES HERE'
                order_number = bill_id_new  # bill number
                msg = EmailMessage()
                msg['Subject'] = str(
                    cname_txt.get()) + ' your bill for bill number ' + order_number + ' is attached'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = str(cphn_txt.get())

                msg.set_content('thank you for shopping with us !')

                files = ["foo.pdf"]  # sample pdf

                for file in files:
                    with open(file, 'rb') as f:
                        file_data = f.read()
                        file_name = bill_id_new + " | Bill Details.pdf"
                    msg.add_attachment(
                        file_data, maintype='application', subtype='octet-stream', filename=file_name)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)

            except Exception as ex_tmp:
                print(ex_tmp)

            # ====================================

            if len(cphn_txt.get()) > 0:
                cphn_txt.delete(0, END)
            cname_txt.delete(0, END)
            discount_txt.delete(0, END)
            discount_txt.insert(0, int(0))

            mstr_df_prd = pd.DataFrame({'pname': [], 'mrp': [], 'barcode': [], 'pid': [
            ], 'quantity': [], 'total': [], 'profit': [], 'total_profit': []})

            bc_list_bill_all = []
            name_list_bill = pd.DataFrame()
            pid_list_bill = pd.DataFrame()
            mrp_list_bill = pd.DataFrame()
            bc_list_bill = pd.DataFrame()

            sac1_e.configure(state="normal")
            sac1_e.delete('1.0', END)

            sac1_e.configure(state="disable")

            sac2_e.configure(state="normal")
            sac2_e.delete('1.0', END)

            sac2_e.configure(state='disable')

            sac3_e.configure(state="normal")
            sac3_e.delete('1.0', END)

            sac3_e.configure(state="disable")

            sac4_e.configure(state="normal")
            sac4_e.delete('1.0', END)

            sac4_e.configure(state='disable')

            total_bill_txt.configure(state='normal')
            total_bill_txt.delete(0, END)
            total_bill_txt.configure(state='disable')

            messagebox.showinfo("BILL ID "+bill_id_new,
                                "Bill generated successfully !")

            bill_qry = "select `bill_id` from bill_details;"
            bill_list_df = pd.read_sql(bill_qry, mycon)
            bill_list_all = bill_list_df['bill_id'].tolist()

            bill_id_new = ''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
            while bill_id_new in bill_list_all:
                bill_id_new = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=8))

            c_bill_txt.configure(state='normal')
            if len(c_bill_txt.get()) > 0:
                c_bill_txt.delete(0, END)

            c_bill_txt.insert(0, bill_id_new)
            c_bill_txt.configure(state='disable')

            generate_btn_lbl.configure(state='normal')

        else:

            messagebox.showinfo("CANNOT GENERATE BILL",
                                "Fill all the details/ add some items first !")

    show_frame()

    generate_btn_lbl = Button(generate_btn, text="Generate Bill", width=20, font=(
        'arial', 14, 'bold'), command=generate_bill_main, bg=btn_p_bg, fg=btn_p_fg,  borderwidth='4')
    generate_btn_lbl.grid(row=0, column=0, pady=5, padx=3)

    total_btn_lbl = Button(total_btn, text="TOTAL AMOUNT", width=20, font=(
        'arial', 14, 'bold'), command=total_amt_bill_gen,  borderwidth='4')
    total_btn_lbl.grid(row=0, column=0, pady=5, padx=3)

    Button(manual_mode, text="ADD ITEM", width=15,  borderwidth='4', font=('arial', 12, 'bold'),
           command=add_product_tobill).grid(row=0, column=2, pady=3, padx=5)

    Button(manual_mode, text="REMOVE", width=15,  borderwidth='4', font=('arial', 12, 'bold'),
           command=remove_item_frombill).grid(row=1, column=2, pady=3, padx=5)
