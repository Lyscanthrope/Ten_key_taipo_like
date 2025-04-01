import numpy as np
import matplotlib.pyplot as plt
import math 

custom={
    #mod
    "SHIFT":[0,0,0,1,0,0,0,1,0,0],
    "CTRL":[0,0,1,0,0,0,1,0,0,0],
    "ALT":[0,1,0,0,0,1,0,0,0,0],
    "GUI":[1,0,0,0,1,0,0,0,0,0],
    #motion
    "LEFT":[0,0,0,1,0,0,0,1,1,0],
    "DOWN":[0,0,1,0,0,0,1,0,1,0],
    "UP":[0,1,0,0,0,1,0,0,1,0],
    "RIGHT":[1,0,0,0,1,0,0,0,1,0],
    #motion_extended
    "PGDOWN":[0,0,0,1,0,0,0,1,0,1],
    "END":[0,0,1,0,0,0,1,0,0,1],
    "HOME":[0,1,0,0,0,1,0,0,0,1],
    "PGUP":[1,0,0,0,1,0,0,0,0,1],
    #tab enter
    "TAB":[0,1,1,1,0,0,0,0,0,0],
    "ENTER":[0,0,0,0,0,1,1,1,0,0],    
    #tab enter
    "DEL":[0,1,1,1,0,0,0,0,1,0],
    "ESC":[0,0,0,0,0,1,1,1,1,0],    
    #tab enter
    "FN":[0,1,1,1,0,0,0,0,0,1],
    "ALTGR":[0,0,0,0,0,1,1,1,0,1],    
    #outer thumb solo letter
    ">":[1,0,0,0,0,0,0,0,0,1],
    "}":[0,1,0,0,0,0,0,0,0,1],
    "]":[0,0,1,0,0,0,0,0,0,1],
    ")":[0,0,0,1,0,0,0,0,0,1],    
    "<":[0,0,0,0,1,0,0,0,0,1],
    "{":[0,0,0,0,0,1,0,0,0,1],
    "[":[0,0,0,0,0,0,1,0,0,1],
    "(":[0,0,0,0,0,0,0,1,0,1],
    #numeric
    "0":[0,0,0,0,0,0,1,1,0,1],
    "1":[0,0,0,0,0,1,0,1,0,1],
    "2":[0,0,0,0,0,1,1,0,0,1],
    "3":[0,0,0,0,1,0,1,0,0,1],
    "4":[0,0,0,0,1,1,0,0,0,1], 
    "5":[0,0,1,1,0,0,0,0,0,1],
    "6":[0,1,0,1,0,0,0,0,0,1],
    "7":[0,1,1,0,0,0,0,0,0,1],
    "8":[1,0,1,0,0,0,0,0,0,1],  
    "9":[1,1,0,0,0,0,0,0,0,1], 
     #fuction keys
    "F1":[0,0,0,0,0,1,0,1,1,1],
    "F2":[0,0,0,0,0,1,1,0,1,1],
    "F3":[0,0,0,0,1,0,1,0,1,1],
    "F4":[0,0,0,0,1,1,0,0,1,1], 
    "F5":[0,0,1,1,0,0,0,0,1,1],
    "F6":[0,1,0,1,0,0,0,0,1,1],
    "F7":[0,1,1,0,0,0,0,0,1,1],
    "F8":[1,0,1,0,0,0,0,0,1,1],  
    "F9":[1,1,0,0,0,0,0,0,1,1], 
    "F10":[0,0,0,0,0,0,1,1,1,1],
    "F11":[0,0,0,0,0,1,1,1,1,1],
    "F12":[0,0,0,0,1,1,1,0,1,1],
}



def add_itot(list_chord,chars):
    """Add two collunms and the it+ot keys, and changes the character list

    Args:
        list_chord (np.array): keypresses
        chars (list): list of characters

    Returns:
        _type_: _description_
    """
    list_chord=np.insert(list_chord,list_chord.shape[1],[False]*len(list_chord),1)
    list_chord=np.insert(list_chord,list_chord.shape[1],[False]*len(list_chord),1)
    it=[False]*(list_chord.shape[1])
    it[-2]=True
    list_chord=np.insert(list_chord,0,it,0)
    ot=[False]*(list_chord.shape[1])
    ot[-1]=True
    list_chord=np.insert(list_chord,0,ot,0)
    extended_chars=chars.copy()
    extended_chars.insert(0,"ot")
    extended_chars.insert(1,"it")
    return list_chord,extended_chars

def add_special_keypress(extended_chord,extended_chars):
    for k,v in custom.items():
        # extended_chord = np.insert(extended_chord, -1, v, axis=0)

        # extended_chars.insert(-1,k)
        extended_chord=np.row_stack([extended_chord,v])
        extended_chars.append(k)

    return extended_chord,extended_chars


def get_list_combo_per_letters(ordered_chords,chars):
    ordered_chords=ordered_chords*1
    list_single_letters={}   
    for i,a in enumerate(ordered_chords):
        index=np.where(a==1)[0]
        if len(index)==1:
            list_single_letters.update({int(index[0]):chars[i]})
        
    list_all_letters={}   
    for i,a in enumerate(ordered_chords):
        mystr=""
        for c in np.where(a==1)[0]:
            mystr=mystr+list_single_letters[c]+" "
        if chars[i]=="'":
            corrected_char="QUOT"
        else:
            corrected_char=chars[i]
        list_all_letters.update({corrected_char:mystr[:-1]})
    return list_all_letters

def plot_layout_extended(extended_layout,chars):
    """Plot the layout of a given list of chords. not very usefull"""
    #reorder the dictionnary
    fig,ax=plt.subplots(math.ceil(len(extended_layout)/4),4,figsize=(9,len(extended_layout)/3))
    ax=ax.flatten()
    for i in range(len(extended_layout)):
        ax[i].imshow(extended_layout[i][:8].reshape((2,4)),aspect="auto",cmap="Blues")
        legend=chars[i]
        if (extended_layout[i][8]):
            legend+=" it"
        if (extended_layout[i][9]):
            legend+=" ot"        
        ax[i].set_title(legend)
        ax[i].set_yticks([])
        ax[i].set_xticks([])
    plt.tight_layout()
    plt.show()

def build_ax(ax,main_keys,main_char,it_char,ot_char,itot_char):
    ax.imshow(main_keys.reshape((2,4)),aspect="auto",cmap="Set2_r")
    legend=""
    if main_char is not None:
        legend+=main_char
    ax.set_title(legend,fontweight='bold')
    ax.text(3.75,0.75,it_char)
    ax.text(4.75,1,ot_char)
    ax.text(4,1.5,itot_char)
    # ax.legend(legend)
    ax.axis('off')
    return ax

def display_extended_keymap(extended_chord,extended_chars):
    _,index_unique=np.unique(extended_chord[:,:8],axis=0,return_index=True)
    l=len(index_unique)
    fig,axes=plt.subplots(math.ceil(l/4),4,figsize=(12,l/3))
    axes=axes.flatten()
    n_box=0
    for idx in np.sort(index_unique):
        # list_index_for_this_combo=[i for i,x in enumerate(extended_chord[:,:8]) if np.array_equal(extended_chord[idx,:8],x)]
        dict_for_this_combo={}
        for i,x in enumerate(extended_chord[:,:8]):
            if np.array_equal(extended_chord[idx,:8],x):
                itot_part=extended_chord[i,8:]
                if np.array_equal(itot_part,[0,0]):
                    k="main"
                    v=extended_chars[i]
                if np.array_equal(itot_part,[1,0]):
                    k="it"
                    v=extended_chars[i]
                if np.array_equal(itot_part,[0,1]):
                    k="ot"
                    v=extended_chars[i]
                if np.array_equal(itot_part,[1,1]):
                    k="itot"
                    v=extended_chars[i]
                dict_for_this_combo.update({k:v})
        empty=""
        build_ax(axes[n_box],extended_chord[idx,:8],dict_for_this_combo.get("main",empty),dict_for_this_combo.get("it",empty),dict_for_this_combo.get("ot",empty),dict_for_this_combo.get("itot",empty))
        n_box+=1
    plt.tight_layout()