[split-summary] id=0 backend=CPU nodes=1 inputs=0
[split-node] split=0 node=0 backend=CPU name=inp_embd op=GET_ROWS
[split-summary] id=1 backend=OpenCL nodes=82 inputs=6
[split-node] split=1 node=0 backend=OpenCL name=norm-0 op=RMS_NORM
[split-node] split=1 node=1 backend=OpenCL name=attn_norm-0 op=MUL
[split-node] split=1 node=2 backend=OpenCL name=q-0 op=MUL_MAT
[split-node] split=1 node=3 backend=OpenCL name=q_pe-0 op=VIEW
[split-node] split=1 node=4 backend=OpenCL name=q_pe-0 op=ROPE
[split-node] split=1 node=5 backend=OpenCL name=q_nope-0 op=VIEW
[split-node] split=1 node=6 backend=OpenCL name=Qcur-0 op=CONCAT
[split-node] split=1 node=7 backend=OpenCL name=kv_cmpr_pe-0 op=MUL_MAT
[split-node] split=1 node=8 backend=OpenCL name=k_pe-0 op=VIEW
[split-node] split=1 node=9 backend=OpenCL name=k_pe-0 op=ROPE
[split-node] split=1 node=10 backend=OpenCL name=node_11 op=REPEAT
[split-node] split=1 node=11 backend=OpenCL name=kv_cmpr-0 op=VIEW
[split-node] split=1 node=12 backend=OpenCL name=norm-0 op=RMS_NORM
[split-node] split=1 node=13 backend=OpenCL name=kv_cmpr-0 op=MUL
[split-node] split=1 node=14 backend=OpenCL name=kv-0 op=MUL_MAT
[split-node] split=1 node=15 backend=OpenCL name=k_nope_view-0 op=VIEW
[split-node] split=1 node=16 backend=OpenCL name=Kcur-0 op=CONCAT
[split-node] split=1 node=17 backend=OpenCL name=Vcur_view-0 op=VIEW
[split-node] split=1 node=18 backend=OpenCL name=Vcur_cont-0 op=CONT
[split-node] split=1 node=19 backend=OpenCL name=Kcur-0 (view) op=VIEW
[split-node] split=1 node=20 backend=OpenCL name=cache_k_l0 (view) op=SET_ROWS
[split-node] split=1 node=21 backend=OpenCL name=Vcur_cont-0 (view) op=VIEW
[split-node] split=1 node=22 backend=OpenCL name=cache_v_l0 (view) op=SET_ROWS
[split-node] split=1 node=23 backend=OpenCL name=Qcur-0 (view) op=VIEW
[split-node] split=1 node=24 backend=OpenCL name=Qcur-0 (view) (permuted) op=PERMUTE
[split-node] split=1 node=25 backend=OpenCL name=cache_k_l0 (view) op=VIEW
[split-node] split=1 node=26 backend=OpenCL name=cache_k_l0 (view) (permuted) op=PERMUTE
[split-node] split=1 node=27 backend=OpenCL name=cache_v_l0 (view) op=VIEW
[split-node] split=1 node=28 backend=OpenCL name=cache_v_l0 (view) (permuted) op=PERMUTE
[split-node] split=1 node=29 backend=OpenCL name= (copy) op=CPY
[split-node] split=1 node=30 backend=OpenCL name=__fattn__-0 op=FLASH_ATTN_BACK
[split-node] split=1 node=31 backend=OpenCL name=kqv_out-0 op=RESHAPE
[split-node] split=1 node=32 backend=OpenCL name=node_33 op=MUL_MAT
[split-node] split=1 node=33 backend=OpenCL name=ffn_inp-0 op=ADD
[split-node] split=1 node=34 backend=OpenCL name=norm-0 op=RMS_NORM
[split-node] split=1 node=35 backend=OpenCL name=ffn_norm-0 op=MUL
[split-node] split=1 node=36 backend=OpenCL name=ffn_gate-0 op=MUL_MAT
[split-node] split=1 node=37 backend=OpenCL name=ffn_up-0 op=MUL_MAT
[split-node] split=1 node=38 backend=OpenCL name=ffn_swiglu-0 op=(null)
[split-node] split=1 node=39 backend=OpenCL name=ffn_out-0 op=MUL_MAT
[split-node] split=1 node=40 backend=OpenCL name=l_out-0 op=ADD
[split-node] split=1 node=41 backend=OpenCL name=norm-1 op=RMS_NORM
[split-node] split=1 node=42 backend=OpenCL name=attn_norm-1 op=MUL
[split-node] split=1 node=43 backend=OpenCL name=q-1 op=MUL_MAT
[split-node] split=1 node=44 backend=OpenCL name=q_pe-1 op=VIEW
[split-node] split=1 node=45 backend=OpenCL name=q_pe-1 op=ROPE
[split-node] split=1 node=46 backend=OpenCL name=q_nope-1 op=VIEW
[split-node] split=1 node=47 backend=OpenCL name=Qcur-1 op=CONCAT
[split-node] split=1 node=48 backend=OpenCL name=kv_cmpr_pe-1 op=MUL_MAT
[split-node] split=1 node=49 backend=OpenCL name=k_pe-1 op=VIEW
[split-node] split=1 node=50 backend=OpenCL name=k_pe-1 op=ROPE
[split-node] split=1 node=51 backend=OpenCL name=node_52 op=REPEAT
[split-node] split=1 node=52 backend=OpenCL name=kv_cmpr-1 op=VIEW
[split-node] split=1 node=53 backend=OpenCL name=norm-1 op=RMS_NORM
[split-node] split=1 node=54 backend=OpenCL name=kv_cmpr-1 op=MUL
[split-node] split=1 node=55 backend=OpenCL name=kv-1 op=MUL_MAT
[split-node] split=1 node=56 backend=OpenCL name=k_nope_view-1 op=VIEW
[split-node] split=1 node=57 backend=OpenCL name=Kcur-1 op=CONCAT
[split-node] split=1 node=58 backend=OpenCL name=Vcur_view-1 op=VIEW
[split-node] split=1 node=59 backend=OpenCL name=Vcur_cont-1 op=CONT
[split-node] split=1 node=60 backend=OpenCL name=Kcur-1 (view) op=VIEW
[split-node] split=1 node=61 backend=OpenCL name=cache_k_l1 (view) op=SET_ROWS
[split-node] split=1 node=62 backend=OpenCL name=Vcur_cont-1 (view) op=VIEW
[split-node] split=1 node=63 backend=OpenCL name=cache_v_l1 (view) op=SET_ROWS
[split-node] split=1 node=64 backend=OpenCL name=Qcur-1 (view) op=VIEW
[split-node] split=1 node=65 backend=OpenCL name=Qcur-1 (view) (permuted) op=PERMUTE
[split-node] split=1 node=66 backend=OpenCL name=cache_k_l1 (view) op=VIEW
[split-node] split=1 node=67 backend=OpenCL name=cache_k_l1 (view) (permuted) op=PERMUTE
[split-node] split=1 node=68 backend=OpenCL name=cache_v_l1 (view) op=VIEW
[split-node] split=1 node=69 backend=OpenCL name=cache_v_l1 (view) (permuted) op=PERMUTE
[split-node] split=1 node=70 backend=OpenCL name=__fattn__-1 op=FLASH_ATTN_BACK
[split-node] split=1 node=71 backend=OpenCL name=kqv_out-1 op=RESHAPE
[split-node] split=1 node=72 backend=OpenCL name=node_73 op=MUL_MAT
[split-node] split=1 node=73 backend=OpenCL name=ffn_inp-1 op=ADD
[split-node] split=1 node=74 backend=OpenCL name=norm-1 op=RMS_NORM
[split-node] split=1 node=75 backend=OpenCL name=ffn_norm-1 op=MUL
[split-node] split=1 node=76 backend=OpenCL name=ffn_moe_logits-1 op=MUL_MAT
[split-node] split=1 node=77 backend=OpenCL name=ffn_moe_probs-1 op=SOFT_MAX
[split-node] split=1 node=78 backend=OpenCL name=ffn_moe_probs-1 (reshaped) op=RESHAPE
[split-node] split=1 node=79 backend=OpenCL name=ffn_moe_argsort-1 op=ARGSORT
[split-node] split=1 node=80 backend=OpenCL name=ffn_moe_topk-1 op=VIEW
[split-node] split=1 node=81 backend=OpenCL name=ffn_moe_weights-1 op=GET_ROWS
[split-input] split=1 name=inp_embd bytes=4194304 backend_dst=OpenCL
[split-input] split=1 name=leaf_4 bytes=2048 backend_dst=OpenCL
[split-input] split=1 name=leaf_8 bytes=4096 backend_dst=OpenCL
[split-input] split=1 name=leaf_10 bytes=4096 backend_dst=OpenCL
[split-input] split=1 name=leaf_12 bytes=1048576 backend_dst=OpenCL
[split-input] split=1 name=ffn_moe_topk-1 bytes=130840 backend_dst=OpenCL
[split-summary] id=2 backend=CPU nodes=2 inputs=1
[split-node] split=2 node=0 backend=CPU name=ffn_moe_weights_scaled-1 op=SCALE
[split-node] split=2 node=1 backend=OpenCL name=ffn_norm-1 (reshaped) op=RESHAPE
[split-input] split=2 name=ffn_moe_weights-1 bytes=12288 backend_dst=CPU
[split-summary] id=3 backend=OpenCL nodes=63 inputs=2
[split-node] split=3 node=0 backend=OpenCL name=ffn_moe_gate-1 op=MUL_MAT_ID
[split-node] split=3 node=1 backend=OpenCL name=ffn_moe_up-1 op=MUL_MAT_ID
[split-node] split=3 node=2 backend=OpenCL name=ffn_moe_weighted-1 op=(null)
[split-node] split=3 node=3 backend=OpenCL name=ffn_moe_down-1 op=MUL_MAT_ID
[split-node] split=3 node=4 backend=OpenCL name=node_89 op=MUL
[split-node] split=3 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=3 node=6 backend=OpenCL name=node_89 (view) op=VIEW
[split-node] split=3 node=7 backend=OpenCL name=node_89 (view) op=VIEW
[split-node] split=3 node=8 backend=OpenCL name=node_89 (view) op=VIEW
[split-node] split=3 node=9 backend=OpenCL name=node_89 (view) op=VIEW
[split-node] split=3 node=10 backend=OpenCL name=node_89 (view) op=VIEW
[split-node] split=3 node=11 backend=OpenCL name=ffn_gate-1 op=MUL_MAT
[split-node] split=3 node=12 backend=OpenCL name=ffn_up-1 op=MUL_MAT
[split-node] split=3 node=13 backend=OpenCL name=ffn_swiglu-1 op=(null)
[split-node] split=3 node=14 backend=OpenCL name=node_99 op=ADD
[split-node] split=3 node=15 backend=OpenCL name=node_100 op=ADD
[split-node] split=3 node=16 backend=OpenCL name=node_101 op=ADD
[split-node] split=3 node=17 backend=OpenCL name=node_102 op=ADD
[split-node] split=3 node=18 backend=OpenCL name=ffn_moe_out-1 op=ADD
[split-node] split=3 node=19 backend=OpenCL name=ffn_shexp-1 op=MUL_MAT
[split-node] split=3 node=20 backend=OpenCL name=ffn_out-1 op=ADD
[split-node] split=3 node=21 backend=OpenCL name=l_out-1 op=ADD
[split-node] split=3 node=22 backend=OpenCL name=norm-2 op=RMS_NORM
[split-node] split=3 node=23 backend=OpenCL name=attn_norm-2 op=MUL
[split-node] split=3 node=24 backend=OpenCL name=q-2 op=MUL_MAT
[split-node] split=3 node=25 backend=OpenCL name=q_pe-2 op=VIEW
[split-node] split=3 node=26 backend=OpenCL name=q_pe-2 op=ROPE
[split-node] split=3 node=27 backend=OpenCL name=q_nope-2 op=VIEW
[split-node] split=3 node=28 backend=OpenCL name=Qcur-2 op=CONCAT
[split-node] split=3 node=29 backend=OpenCL name=kv_cmpr_pe-2 op=MUL_MAT
[split-node] split=3 node=30 backend=OpenCL name=k_pe-2 op=VIEW
[split-node] split=3 node=31 backend=OpenCL name=k_pe-2 op=ROPE
[split-node] split=3 node=32 backend=OpenCL name=node_117 op=REPEAT
[split-node] split=3 node=33 backend=OpenCL name=kv_cmpr-2 op=VIEW
[split-node] split=3 node=34 backend=OpenCL name=norm-2 op=RMS_NORM
[split-node] split=3 node=35 backend=OpenCL name=kv_cmpr-2 op=MUL
[split-node] split=3 node=36 backend=OpenCL name=kv-2 op=MUL_MAT
[split-node] split=3 node=37 backend=OpenCL name=k_nope_view-2 op=VIEW
[split-node] split=3 node=38 backend=OpenCL name=Kcur-2 op=CONCAT
[split-node] split=3 node=39 backend=OpenCL name=Vcur_view-2 op=VIEW
[split-node] split=3 node=40 backend=OpenCL name=Vcur_cont-2 op=CONT
[split-node] split=3 node=41 backend=OpenCL name=Kcur-2 (view) op=VIEW
[split-node] split=3 node=42 backend=OpenCL name=cache_k_l2 (view) op=SET_ROWS
[split-node] split=3 node=43 backend=OpenCL name=Vcur_cont-2 (view) op=VIEW
[split-node] split=3 node=44 backend=OpenCL name=cache_v_l2 (view) op=SET_ROWS
[split-node] split=3 node=45 backend=OpenCL name=Qcur-2 (view) op=VIEW
[split-node] split=3 node=46 backend=OpenCL name=Qcur-2 (view) (permuted) op=PERMUTE
[split-node] split=3 node=47 backend=OpenCL name=cache_k_l2 (view) op=VIEW
[split-node] split=3 node=48 backend=OpenCL name=cache_k_l2 (view) (permuted) op=PERMUTE
[split-node] split=3 node=49 backend=OpenCL name=cache_v_l2 (view) op=VIEW
[split-node] split=3 node=50 backend=OpenCL name=cache_v_l2 (view) (permuted) op=PERMUTE
[split-node] split=3 node=51 backend=OpenCL name=__fattn__-2 op=FLASH_ATTN_BACK
[split-node] split=3 node=52 backend=OpenCL name=kqv_out-2 op=RESHAPE
[split-node] split=3 node=53 backend=OpenCL name=node_138 op=MUL_MAT
[split-node] split=3 node=54 backend=OpenCL name=ffn_inp-2 op=ADD
[split-node] split=3 node=55 backend=OpenCL name=norm-2 op=RMS_NORM
[split-node] split=3 node=56 backend=OpenCL name=ffn_norm-2 op=MUL
[split-node] split=3 node=57 backend=OpenCL name=ffn_moe_logits-2 op=MUL_MAT
[split-node] split=3 node=58 backend=OpenCL name=ffn_moe_probs-2 op=SOFT_MAX
[split-node] split=3 node=59 backend=OpenCL name=ffn_moe_probs-2 (reshaped) op=RESHAPE
[split-node] split=3 node=60 backend=OpenCL name=ffn_moe_argsort-2 op=ARGSORT
[split-node] split=3 node=61 backend=OpenCL name=ffn_moe_topk-2 op=VIEW
[split-node] split=3 node=62 backend=OpenCL name=ffn_moe_weights-2 op=GET_ROWS
[split-input] split=3 name=ffn_moe_weights_scaled-1 bytes=12288 backend_dst=OpenCL
[split-input] split=3 name=ffn_moe_topk-2 bytes=130840 backend_dst=OpenCL
[split-summary] id=4 backend=CPU nodes=2 inputs=1
[split-node] split=4 node=0 backend=CPU name=ffn_moe_weights_scaled-2 op=SCALE
[split-node] split=4 node=1 backend=OpenCL name=ffn_norm-2 (reshaped) op=RESHAPE
[split-input] split=4 name=ffn_moe_weights-2 bytes=12288 backend_dst=CPU
[split-summary] id=5 backend=OpenCL nodes=63 inputs=2
[split-node] split=5 node=0 backend=OpenCL name=ffn_moe_gate-2 op=MUL_MAT_ID
[split-node] split=5 node=1 backend=OpenCL name=ffn_moe_up-2 op=MUL_MAT_ID
[split-node] split=5 node=2 backend=OpenCL name=ffn_moe_weighted-2 op=(null)
[split-node] split=5 node=3 backend=OpenCL name=ffn_moe_down-2 op=MUL_MAT_ID
[split-node] split=5 node=4 backend=OpenCL name=node_154 op=MUL
[split-node] split=5 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=5 node=6 backend=OpenCL name=node_154 (view) op=VIEW
[split-node] split=5 node=7 backend=OpenCL name=node_154 (view) op=VIEW
[split-node] split=5 node=8 backend=OpenCL name=node_154 (view) op=VIEW
[split-node] split=5 node=9 backend=OpenCL name=node_154 (view) op=VIEW
[split-node] split=5 node=10 backend=OpenCL name=node_154 (view) op=VIEW
[split-node] split=5 node=11 backend=OpenCL name=ffn_gate-2 op=MUL_MAT
[split-node] split=5 node=12 backend=OpenCL name=ffn_up-2 op=MUL_MAT
[split-node] split=5 node=13 backend=OpenCL name=ffn_swiglu-2 op=(null)
[split-node] split=5 node=14 backend=OpenCL name=node_164 op=ADD
[split-node] split=5 node=15 backend=OpenCL name=node_165 op=ADD
[split-node] split=5 node=16 backend=OpenCL name=node_166 op=ADD
[split-node] split=5 node=17 backend=OpenCL name=node_167 op=ADD
[split-node] split=5 node=18 backend=OpenCL name=ffn_moe_out-2 op=ADD
[split-node] split=5 node=19 backend=OpenCL name=ffn_shexp-2 op=MUL_MAT
[split-node] split=5 node=20 backend=OpenCL name=ffn_out-2 op=ADD
[split-node] split=5 node=21 backend=OpenCL name=l_out-2 op=ADD
[split-node] split=5 node=22 backend=OpenCL name=norm-3 op=RMS_NORM
[split-node] split=5 node=23 backend=OpenCL name=attn_norm-3 op=MUL
[split-node] split=5 node=24 backend=OpenCL name=q-3 op=MUL_MAT
[split-node] split=5 node=25 backend=OpenCL name=q_pe-3 op=VIEW
[split-node] split=5 node=26 backend=OpenCL name=q_pe-3 op=ROPE
[split-node] split=5 node=27 backend=OpenCL name=q_nope-3 op=VIEW
[split-node] split=5 node=28 backend=OpenCL name=Qcur-3 op=CONCAT
[split-node] split=5 node=29 backend=OpenCL name=kv_cmpr_pe-3 op=MUL_MAT
[split-node] split=5 node=30 backend=OpenCL name=k_pe-3 op=VIEW
[split-node] split=5 node=31 backend=OpenCL name=k_pe-3 op=ROPE
[split-node] split=5 node=32 backend=OpenCL name=node_182 op=REPEAT
[split-node] split=5 node=33 backend=OpenCL name=kv_cmpr-3 op=VIEW
[split-node] split=5 node=34 backend=OpenCL name=norm-3 op=RMS_NORM
[split-node] split=5 node=35 backend=OpenCL name=kv_cmpr-3 op=MUL
[split-node] split=5 node=36 backend=OpenCL name=kv-3 op=MUL_MAT
[split-node] split=5 node=37 backend=OpenCL name=k_nope_view-3 op=VIEW
[split-node] split=5 node=38 backend=OpenCL name=Kcur-3 op=CONCAT
[split-node] split=5 node=39 backend=OpenCL name=Vcur_view-3 op=VIEW
[split-node] split=5 node=40 backend=OpenCL name=Vcur_cont-3 op=CONT
[split-node] split=5 node=41 backend=OpenCL name=Kcur-3 (view) op=VIEW
[split-node] split=5 node=42 backend=OpenCL name=cache_k_l3 (view) op=SET_ROWS
[split-node] split=5 node=43 backend=OpenCL name=Vcur_cont-3 (view) op=VIEW
[split-node] split=5 node=44 backend=OpenCL name=cache_v_l3 (view) op=SET_ROWS
[split-node] split=5 node=45 backend=OpenCL name=Qcur-3 (view) op=VIEW
[split-node] split=5 node=46 backend=OpenCL name=Qcur-3 (view) (permuted) op=PERMUTE
[split-node] split=5 node=47 backend=OpenCL name=cache_k_l3 (view) op=VIEW
[split-node] split=5 node=48 backend=OpenCL name=cache_k_l3 (view) (permuted) op=PERMUTE
[split-node] split=5 node=49 backend=OpenCL name=cache_v_l3 (view) op=VIEW
[split-node] split=5 node=50 backend=OpenCL name=cache_v_l3 (view) (permuted) op=PERMUTE
[split-node] split=5 node=51 backend=OpenCL name=__fattn__-3 op=FLASH_ATTN_BACK
[split-node] split=5 node=52 backend=OpenCL name=kqv_out-3 op=RESHAPE
[split-node] split=5 node=53 backend=OpenCL name=node_203 op=MUL_MAT
[split-node] split=5 node=54 backend=OpenCL name=ffn_inp-3 op=ADD
[split-node] split=5 node=55 backend=OpenCL name=norm-3 op=RMS_NORM
[split-node] split=5 node=56 backend=OpenCL name=ffn_norm-3 op=MUL
[split-node] split=5 node=57 backend=OpenCL name=ffn_moe_logits-3 op=MUL_MAT
[split-node] split=5 node=58 backend=OpenCL name=ffn_moe_probs-3 op=SOFT_MAX
[split-node] split=5 node=59 backend=OpenCL name=ffn_moe_probs-3 (reshaped) op=RESHAPE
[split-node] split=5 node=60 backend=OpenCL name=ffn_moe_argsort-3 op=ARGSORT
[split-node] split=5 node=61 backend=OpenCL name=ffn_moe_topk-3 op=VIEW
[split-node] split=5 node=62 backend=OpenCL name=ffn_moe_weights-3 op=GET_ROWS
[split-input] split=5 name=ffn_moe_weights_scaled-2 bytes=12288 backend_dst=OpenCL
[split-input] split=5 name=ffn_moe_topk-3 bytes=130840 backend_dst=OpenCL
[split-summary] id=6 backend=CPU nodes=2 inputs=1
[split-node] split=6 node=0 backend=CPU name=ffn_moe_weights_scaled-3 op=SCALE
[split-node] split=6 node=1 backend=OpenCL name=ffn_norm-3 (reshaped) op=RESHAPE
[split-input] split=6 name=ffn_moe_weights-3 bytes=12288 backend_dst=CPU
[split-summary] id=7 backend=OpenCL nodes=63 inputs=2
[split-node] split=7 node=0 backend=OpenCL name=ffn_moe_gate-3 op=MUL_MAT_ID
[split-node] split=7 node=1 backend=OpenCL name=ffn_moe_up-3 op=MUL_MAT_ID
[split-node] split=7 node=2 backend=OpenCL name=ffn_moe_weighted-3 op=(null)
[split-node] split=7 node=3 backend=OpenCL name=ffn_moe_down-3 op=MUL_MAT_ID
[split-node] split=7 node=4 backend=OpenCL name=node_219 op=MUL
[split-node] split=7 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=7 node=6 backend=OpenCL name=node_219 (view) op=VIEW
[split-node] split=7 node=7 backend=OpenCL name=node_219 (view) op=VIEW
[split-node] split=7 node=8 backend=OpenCL name=node_219 (view) op=VIEW
[split-node] split=7 node=9 backend=OpenCL name=node_219 (view) op=VIEW
[split-node] split=7 node=10 backend=OpenCL name=node_219 (view) op=VIEW
[split-node] split=7 node=11 backend=OpenCL name=ffn_gate-3 op=MUL_MAT
[split-node] split=7 node=12 backend=OpenCL name=ffn_up-3 op=MUL_MAT
[split-node] split=7 node=13 backend=OpenCL name=ffn_swiglu-3 op=(null)
[split-node] split=7 node=14 backend=OpenCL name=node_229 op=ADD
[split-node] split=7 node=15 backend=OpenCL name=node_230 op=ADD
[split-node] split=7 node=16 backend=OpenCL name=node_231 op=ADD
[split-node] split=7 node=17 backend=OpenCL name=node_232 op=ADD
[split-node] split=7 node=18 backend=OpenCL name=ffn_moe_out-3 op=ADD
[split-node] split=7 node=19 backend=OpenCL name=ffn_shexp-3 op=MUL_MAT
[split-node] split=7 node=20 backend=OpenCL name=ffn_out-3 op=ADD
[split-node] split=7 node=21 backend=OpenCL name=l_out-3 op=ADD
[split-node] split=7 node=22 backend=OpenCL name=norm-4 op=RMS_NORM
[split-node] split=7 node=23 backend=OpenCL name=attn_norm-4 op=MUL
[split-node] split=7 node=24 backend=OpenCL name=q-4 op=MUL_MAT
[split-node] split=7 node=25 backend=OpenCL name=q_pe-4 op=VIEW
[split-node] split=7 node=26 backend=OpenCL name=q_pe-4 op=ROPE
[split-node] split=7 node=27 backend=OpenCL name=q_nope-4 op=VIEW
[split-node] split=7 node=28 backend=OpenCL name=Qcur-4 op=CONCAT
[split-node] split=7 node=29 backend=OpenCL name=kv_cmpr_pe-4 op=MUL_MAT
[split-node] split=7 node=30 backend=OpenCL name=k_pe-4 op=VIEW
[split-node] split=7 node=31 backend=OpenCL name=k_pe-4 op=ROPE
[split-node] split=7 node=32 backend=OpenCL name=node_247 op=REPEAT
[split-node] split=7 node=33 backend=OpenCL name=kv_cmpr-4 op=VIEW
[split-node] split=7 node=34 backend=OpenCL name=norm-4 op=RMS_NORM
[split-node] split=7 node=35 backend=OpenCL name=kv_cmpr-4 op=MUL
[split-node] split=7 node=36 backend=OpenCL name=kv-4 op=MUL_MAT
[split-node] split=7 node=37 backend=OpenCL name=k_nope_view-4 op=VIEW
[split-node] split=7 node=38 backend=OpenCL name=Kcur-4 op=CONCAT
[split-node] split=7 node=39 backend=OpenCL name=Vcur_view-4 op=VIEW
[split-node] split=7 node=40 backend=OpenCL name=Vcur_cont-4 op=CONT
[split-node] split=7 node=41 backend=OpenCL name=Kcur-4 (view) op=VIEW
[split-node] split=7 node=42 backend=OpenCL name=cache_k_l4 (view) op=SET_ROWS
[split-node] split=7 node=43 backend=OpenCL name=Vcur_cont-4 (view) op=VIEW
[split-node] split=7 node=44 backend=OpenCL name=cache_v_l4 (view) op=SET_ROWS
[split-node] split=7 node=45 backend=OpenCL name=Qcur-4 (view) op=VIEW
[split-node] split=7 node=46 backend=OpenCL name=Qcur-4 (view) (permuted) op=PERMUTE
[split-node] split=7 node=47 backend=OpenCL name=cache_k_l4 (view) op=VIEW
[split-node] split=7 node=48 backend=OpenCL name=cache_k_l4 (view) (permuted) op=PERMUTE
[split-node] split=7 node=49 backend=OpenCL name=cache_v_l4 (view) op=VIEW
[split-node] split=7 node=50 backend=OpenCL name=cache_v_l4 (view) (permuted) op=PERMUTE
[split-node] split=7 node=51 backend=OpenCL name=__fattn__-4 op=FLASH_ATTN_BACK
[split-node] split=7 node=52 backend=OpenCL name=kqv_out-4 op=RESHAPE
[split-node] split=7 node=53 backend=OpenCL name=node_268 op=MUL_MAT
[split-node] split=7 node=54 backend=OpenCL name=ffn_inp-4 op=ADD
[split-node] split=7 node=55 backend=OpenCL name=norm-4 op=RMS_NORM
[split-node] split=7 node=56 backend=OpenCL name=ffn_norm-4 op=MUL
[split-node] split=7 node=57 backend=OpenCL name=ffn_moe_logits-4 op=MUL_MAT
[split-node] split=7 node=58 backend=OpenCL name=ffn_moe_probs-4 op=SOFT_MAX
[split-node] split=7 node=59 backend=OpenCL name=ffn_moe_probs-4 (reshaped) op=RESHAPE
[split-node] split=7 node=60 backend=OpenCL name=ffn_moe_argsort-4 op=ARGSORT
[split-node] split=7 node=61 backend=OpenCL name=ffn_moe_topk-4 op=VIEW
[split-node] split=7 node=62 backend=OpenCL name=ffn_moe_weights-4 op=GET_ROWS
[split-input] split=7 name=ffn_moe_weights_scaled-3 bytes=12288 backend_dst=OpenCL
[split-input] split=7 name=ffn_moe_topk-4 bytes=130840 backend_dst=OpenCL
[split-summary] id=8 backend=CPU nodes=2 inputs=1
[split-node] split=8 node=0 backend=CPU name=ffn_moe_weights_scaled-4 op=SCALE
[split-node] split=8 node=1 backend=OpenCL name=ffn_norm-4 (reshaped) op=RESHAPE
[split-input] split=8 name=ffn_moe_weights-4 bytes=12288 backend_dst=CPU
[split-summary] id=9 backend=OpenCL nodes=63 inputs=2
[split-node] split=9 node=0 backend=OpenCL name=ffn_moe_gate-4 op=MUL_MAT_ID
[split-node] split=9 node=1 backend=OpenCL name=ffn_moe_up-4 op=MUL_MAT_ID
[split-node] split=9 node=2 backend=OpenCL name=ffn_moe_weighted-4 op=(null)
[split-node] split=9 node=3 backend=OpenCL name=ffn_moe_down-4 op=MUL_MAT_ID
[split-node] split=9 node=4 backend=OpenCL name=node_284 op=MUL
[split-node] split=9 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=9 node=6 backend=OpenCL name=node_284 (view) op=VIEW
[split-node] split=9 node=7 backend=OpenCL name=node_284 (view) op=VIEW
[split-node] split=9 node=8 backend=OpenCL name=node_284 (view) op=VIEW
[split-node] split=9 node=9 backend=OpenCL name=node_284 (view) op=VIEW
[split-node] split=9 node=10 backend=OpenCL name=node_284 (view) op=VIEW
[split-node] split=9 node=11 backend=OpenCL name=ffn_gate-4 op=MUL_MAT
[split-node] split=9 node=12 backend=OpenCL name=ffn_up-4 op=MUL_MAT
[split-node] split=9 node=13 backend=OpenCL name=ffn_swiglu-4 op=(null)
[split-node] split=9 node=14 backend=OpenCL name=node_294 op=ADD
[split-node] split=9 node=15 backend=OpenCL name=node_295 op=ADD
[split-node] split=9 node=16 backend=OpenCL name=node_296 op=ADD
[split-node] split=9 node=17 backend=OpenCL name=node_297 op=ADD
[split-node] split=9 node=18 backend=OpenCL name=ffn_moe_out-4 op=ADD
[split-node] split=9 node=19 backend=OpenCL name=ffn_shexp-4 op=MUL_MAT
[split-node] split=9 node=20 backend=OpenCL name=ffn_out-4 op=ADD
[split-node] split=9 node=21 backend=OpenCL name=l_out-4 op=ADD
[split-node] split=9 node=22 backend=OpenCL name=norm-5 op=RMS_NORM
[split-node] split=9 node=23 backend=OpenCL name=attn_norm-5 op=MUL
[split-node] split=9 node=24 backend=OpenCL name=q-5 op=MUL_MAT
[split-node] split=9 node=25 backend=OpenCL name=q_pe-5 op=VIEW
[split-node] split=9 node=26 backend=OpenCL name=q_pe-5 op=ROPE
[split-node] split=9 node=27 backend=OpenCL name=q_nope-5 op=VIEW
[split-node] split=9 node=28 backend=OpenCL name=Qcur-5 op=CONCAT
[split-node] split=9 node=29 backend=OpenCL name=kv_cmpr_pe-5 op=MUL_MAT
[split-node] split=9 node=30 backend=OpenCL name=k_pe-5 op=VIEW
[split-node] split=9 node=31 backend=OpenCL name=k_pe-5 op=ROPE
[split-node] split=9 node=32 backend=OpenCL name=node_312 op=REPEAT
[split-node] split=9 node=33 backend=OpenCL name=kv_cmpr-5 op=VIEW
[split-node] split=9 node=34 backend=OpenCL name=norm-5 op=RMS_NORM
[split-node] split=9 node=35 backend=OpenCL name=kv_cmpr-5 op=MUL
[split-node] split=9 node=36 backend=OpenCL name=kv-5 op=MUL_MAT
[split-node] split=9 node=37 backend=OpenCL name=k_nope_view-5 op=VIEW
[split-node] split=9 node=38 backend=OpenCL name=Kcur-5 op=CONCAT
[split-node] split=9 node=39 backend=OpenCL name=Vcur_view-5 op=VIEW
[split-node] split=9 node=40 backend=OpenCL name=Vcur_cont-5 op=CONT
[split-node] split=9 node=41 backend=OpenCL name=Kcur-5 (view) op=VIEW
[split-node] split=9 node=42 backend=OpenCL name=cache_k_l5 (view) op=SET_ROWS
[split-node] split=9 node=43 backend=OpenCL name=Vcur_cont-5 (view) op=VIEW
[split-node] split=9 node=44 backend=OpenCL name=cache_v_l5 (view) op=SET_ROWS
[split-node] split=9 node=45 backend=OpenCL name=Qcur-5 (view) op=VIEW
[split-node] split=9 node=46 backend=OpenCL name=Qcur-5 (view) (permuted) op=PERMUTE
[split-node] split=9 node=47 backend=OpenCL name=cache_k_l5 (view) op=VIEW
[split-node] split=9 node=48 backend=OpenCL name=cache_k_l5 (view) (permuted) op=PERMUTE
[split-node] split=9 node=49 backend=OpenCL name=cache_v_l5 (view) op=VIEW
[split-node] split=9 node=50 backend=OpenCL name=cache_v_l5 (view) (permuted) op=PERMUTE
[split-node] split=9 node=51 backend=OpenCL name=__fattn__-5 op=FLASH_ATTN_BACK
[split-node] split=9 node=52 backend=OpenCL name=kqv_out-5 op=RESHAPE
[split-node] split=9 node=53 backend=OpenCL name=node_333 op=MUL_MAT
[split-node] split=9 node=54 backend=OpenCL name=ffn_inp-5 op=ADD
[split-node] split=9 node=55 backend=OpenCL name=norm-5 op=RMS_NORM
[split-node] split=9 node=56 backend=OpenCL name=ffn_norm-5 op=MUL
[split-node] split=9 node=57 backend=OpenCL name=ffn_moe_logits-5 op=MUL_MAT
[split-node] split=9 node=58 backend=OpenCL name=ffn_moe_probs-5 op=SOFT_MAX
[split-node] split=9 node=59 backend=OpenCL name=ffn_moe_probs-5 (reshaped) op=RESHAPE
[split-node] split=9 node=60 backend=OpenCL name=ffn_moe_argsort-5 op=ARGSORT
[split-node] split=9 node=61 backend=OpenCL name=ffn_moe_topk-5 op=VIEW
[split-node] split=9 node=62 backend=OpenCL name=ffn_moe_weights-5 op=GET_ROWS
[split-input] split=9 name=ffn_moe_weights_scaled-4 bytes=12288 backend_dst=OpenCL
[split-input] split=9 name=ffn_moe_topk-5 bytes=130840 backend_dst=OpenCL
[split-summary] id=10 backend=CPU nodes=2 inputs=1
[split-node] split=10 node=0 backend=CPU name=ffn_moe_weights_scaled-5 op=SCALE
[split-node] split=10 node=1 backend=OpenCL name=ffn_norm-5 (reshaped) op=RESHAPE
[split-input] split=10 name=ffn_moe_weights-5 bytes=12288 backend_dst=CPU
[split-summary] id=11 backend=OpenCL nodes=63 inputs=2
[split-node] split=11 node=0 backend=OpenCL name=ffn_moe_gate-5 op=MUL_MAT_ID
[split-node] split=11 node=1 backend=OpenCL name=ffn_moe_up-5 op=MUL_MAT_ID
[split-node] split=11 node=2 backend=OpenCL name=ffn_moe_weighted-5 op=(null)
[split-node] split=11 node=3 backend=OpenCL name=ffn_moe_down-5 op=MUL_MAT_ID
[split-node] split=11 node=4 backend=OpenCL name=node_349 op=MUL
[split-node] split=11 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=11 node=6 backend=OpenCL name=node_349 (view) op=VIEW
[split-node] split=11 node=7 backend=OpenCL name=node_349 (view) op=VIEW
[split-node] split=11 node=8 backend=OpenCL name=node_349 (view) op=VIEW
[split-node] split=11 node=9 backend=OpenCL name=node_349 (view) op=VIEW
[split-node] split=11 node=10 backend=OpenCL name=node_349 (view) op=VIEW
[split-node] split=11 node=11 backend=OpenCL name=ffn_gate-5 op=MUL_MAT
[split-node] split=11 node=12 backend=OpenCL name=ffn_up-5 op=MUL_MAT
[split-node] split=11 node=13 backend=OpenCL name=ffn_swiglu-5 op=(null)
[split-node] split=11 node=14 backend=OpenCL name=node_359 op=ADD
[split-node] split=11 node=15 backend=OpenCL name=node_360 op=ADD
[split-node] split=11 node=16 backend=OpenCL name=node_361 op=ADD
[split-node] split=11 node=17 backend=OpenCL name=node_362 op=ADD
[split-node] split=11 node=18 backend=OpenCL name=ffn_moe_out-5 op=ADD
[split-node] split=11 node=19 backend=OpenCL name=ffn_shexp-5 op=MUL_MAT
[split-node] split=11 node=20 backend=OpenCL name=ffn_out-5 op=ADD
[split-node] split=11 node=21 backend=OpenCL name=l_out-5 op=ADD
[split-node] split=11 node=22 backend=OpenCL name=norm-6 op=RMS_NORM
[split-node] split=11 node=23 backend=OpenCL name=attn_norm-6 op=MUL
[split-node] split=11 node=24 backend=OpenCL name=q-6 op=MUL_MAT
[split-node] split=11 node=25 backend=OpenCL name=q_pe-6 op=VIEW
[split-node] split=11 node=26 backend=OpenCL name=q_pe-6 op=ROPE
[split-node] split=11 node=27 backend=OpenCL name=q_nope-6 op=VIEW
[split-node] split=11 node=28 backend=OpenCL name=Qcur-6 op=CONCAT
[split-node] split=11 node=29 backend=OpenCL name=kv_cmpr_pe-6 op=MUL_MAT
[split-node] split=11 node=30 backend=OpenCL name=k_pe-6 op=VIEW
[split-node] split=11 node=31 backend=OpenCL name=k_pe-6 op=ROPE
[split-node] split=11 node=32 backend=OpenCL name=node_377 op=REPEAT
[split-node] split=11 node=33 backend=OpenCL name=kv_cmpr-6 op=VIEW
[split-node] split=11 node=34 backend=OpenCL name=norm-6 op=RMS_NORM
[split-node] split=11 node=35 backend=OpenCL name=kv_cmpr-6 op=MUL
[split-node] split=11 node=36 backend=OpenCL name=kv-6 op=MUL_MAT
[split-node] split=11 node=37 backend=OpenCL name=k_nope_view-6 op=VIEW
[split-node] split=11 node=38 backend=OpenCL name=Kcur-6 op=CONCAT
[split-node] split=11 node=39 backend=OpenCL name=Vcur_view-6 op=VIEW
[split-node] split=11 node=40 backend=OpenCL name=Vcur_cont-6 op=CONT
[split-node] split=11 node=41 backend=OpenCL name=Kcur-6 (view) op=VIEW
[split-node] split=11 node=42 backend=OpenCL name=cache_k_l6 (view) op=SET_ROWS
[split-node] split=11 node=43 backend=OpenCL name=Vcur_cont-6 (view) op=VIEW
[split-node] split=11 node=44 backend=OpenCL name=cache_v_l6 (view) op=SET_ROWS
[split-node] split=11 node=45 backend=OpenCL name=Qcur-6 (view) op=VIEW
[split-node] split=11 node=46 backend=OpenCL name=Qcur-6 (view) (permuted) op=PERMUTE
[split-node] split=11 node=47 backend=OpenCL name=cache_k_l6 (view) op=VIEW
[split-node] split=11 node=48 backend=OpenCL name=cache_k_l6 (view) (permuted) op=PERMUTE
[split-node] split=11 node=49 backend=OpenCL name=cache_v_l6 (view) op=VIEW
[split-node] split=11 node=50 backend=OpenCL name=cache_v_l6 (view) (permuted) op=PERMUTE
[split-node] split=11 node=51 backend=OpenCL name=__fattn__-6 op=FLASH_ATTN_BACK
[split-node] split=11 node=52 backend=OpenCL name=kqv_out-6 op=RESHAPE
[split-node] split=11 node=53 backend=OpenCL name=node_398 op=MUL_MAT
[split-node] split=11 node=54 backend=OpenCL name=ffn_inp-6 op=ADD
[split-node] split=11 node=55 backend=OpenCL name=norm-6 op=RMS_NORM
[split-node] split=11 node=56 backend=OpenCL name=ffn_norm-6 op=MUL
[split-node] split=11 node=57 backend=OpenCL name=ffn_moe_logits-6 op=MUL_MAT
[split-node] split=11 node=58 backend=OpenCL name=ffn_moe_probs-6 op=SOFT_MAX
[split-node] split=11 node=59 backend=OpenCL name=ffn_moe_probs-6 (reshaped) op=RESHAPE
[split-node] split=11 node=60 backend=OpenCL name=ffn_moe_argsort-6 op=ARGSORT
[split-node] split=11 node=61 backend=OpenCL name=ffn_moe_topk-6 op=VIEW
[split-node] split=11 node=62 backend=OpenCL name=ffn_moe_weights-6 op=GET_ROWS
[split-input] split=11 name=ffn_moe_weights_scaled-5 bytes=12288 backend_dst=OpenCL
[split-input] split=11 name=ffn_moe_topk-6 bytes=130840 backend_dst=OpenCL
[split-summary] id=12 backend=CPU nodes=2 inputs=1
[split-node] split=12 node=0 backend=CPU name=ffn_moe_weights_scaled-6 op=SCALE
[split-node] split=12 node=1 backend=OpenCL name=ffn_norm-6 (reshaped) op=RESHAPE
[split-input] split=12 name=ffn_moe_weights-6 bytes=12288 backend_dst=CPU
[split-summary] id=13 backend=OpenCL nodes=63 inputs=2
[split-node] split=13 node=0 backend=OpenCL name=ffn_moe_gate-6 op=MUL_MAT_ID
[split-node] split=13 node=1 backend=OpenCL name=ffn_moe_up-6 op=MUL_MAT_ID
[split-node] split=13 node=2 backend=OpenCL name=ffn_moe_weighted-6 op=(null)
[split-node] split=13 node=3 backend=OpenCL name=ffn_moe_down-6 op=MUL_MAT_ID
[split-node] split=13 node=4 backend=OpenCL name=node_414 op=MUL
[split-node] split=13 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=13 node=6 backend=OpenCL name=node_414 (view) op=VIEW
[split-node] split=13 node=7 backend=OpenCL name=node_414 (view) op=VIEW
[split-node] split=13 node=8 backend=OpenCL name=node_414 (view) op=VIEW
[split-node] split=13 node=9 backend=OpenCL name=node_414 (view) op=VIEW
[split-node] split=13 node=10 backend=OpenCL name=node_414 (view) op=VIEW
[split-node] split=13 node=11 backend=OpenCL name=ffn_gate-6 op=MUL_MAT
[split-node] split=13 node=12 backend=OpenCL name=ffn_up-6 op=MUL_MAT
[split-node] split=13 node=13 backend=OpenCL name=ffn_swiglu-6 op=(null)
[split-node] split=13 node=14 backend=OpenCL name=node_424 op=ADD
[split-node] split=13 node=15 backend=OpenCL name=node_425 op=ADD
[split-node] split=13 node=16 backend=OpenCL name=node_426 op=ADD
[split-node] split=13 node=17 backend=OpenCL name=node_427 op=ADD
[split-node] split=13 node=18 backend=OpenCL name=ffn_moe_out-6 op=ADD
[split-node] split=13 node=19 backend=OpenCL name=ffn_shexp-6 op=MUL_MAT
[split-node] split=13 node=20 backend=OpenCL name=ffn_out-6 op=ADD
[split-node] split=13 node=21 backend=OpenCL name=l_out-6 op=ADD
[split-node] split=13 node=22 backend=OpenCL name=norm-7 op=RMS_NORM
[split-node] split=13 node=23 backend=OpenCL name=attn_norm-7 op=MUL
[split-node] split=13 node=24 backend=OpenCL name=q-7 op=MUL_MAT
[split-node] split=13 node=25 backend=OpenCL name=q_pe-7 op=VIEW
[split-node] split=13 node=26 backend=OpenCL name=q_pe-7 op=ROPE
[split-node] split=13 node=27 backend=OpenCL name=q_nope-7 op=VIEW
[split-node] split=13 node=28 backend=OpenCL name=Qcur-7 op=CONCAT
[split-node] split=13 node=29 backend=OpenCL name=kv_cmpr_pe-7 op=MUL_MAT
[split-node] split=13 node=30 backend=OpenCL name=k_pe-7 op=VIEW
[split-node] split=13 node=31 backend=OpenCL name=k_pe-7 op=ROPE
[split-node] split=13 node=32 backend=OpenCL name=node_442 op=REPEAT
[split-node] split=13 node=33 backend=OpenCL name=kv_cmpr-7 op=VIEW
[split-node] split=13 node=34 backend=OpenCL name=norm-7 op=RMS_NORM
[split-node] split=13 node=35 backend=OpenCL name=kv_cmpr-7 op=MUL
[split-node] split=13 node=36 backend=OpenCL name=kv-7 op=MUL_MAT
[split-node] split=13 node=37 backend=OpenCL name=k_nope_view-7 op=VIEW
[split-node] split=13 node=38 backend=OpenCL name=Kcur-7 op=CONCAT
[split-node] split=13 node=39 backend=OpenCL name=Vcur_view-7 op=VIEW
[split-node] split=13 node=40 backend=OpenCL name=Vcur_cont-7 op=CONT
[split-node] split=13 node=41 backend=OpenCL name=Kcur-7 (view) op=VIEW
[split-node] split=13 node=42 backend=OpenCL name=cache_k_l7 (view) op=SET_ROWS
[split-node] split=13 node=43 backend=OpenCL name=Vcur_cont-7 (view) op=VIEW
[split-node] split=13 node=44 backend=OpenCL name=cache_v_l7 (view) op=SET_ROWS
[split-node] split=13 node=45 backend=OpenCL name=Qcur-7 (view) op=VIEW
[split-node] split=13 node=46 backend=OpenCL name=Qcur-7 (view) (permuted) op=PERMUTE
[split-node] split=13 node=47 backend=OpenCL name=cache_k_l7 (view) op=VIEW
[split-node] split=13 node=48 backend=OpenCL name=cache_k_l7 (view) (permuted) op=PERMUTE
[split-node] split=13 node=49 backend=OpenCL name=cache_v_l7 (view) op=VIEW
[split-node] split=13 node=50 backend=OpenCL name=cache_v_l7 (view) (permuted) op=PERMUTE
[split-node] split=13 node=51 backend=OpenCL name=__fattn__-7 op=FLASH_ATTN_BACK
[split-node] split=13 node=52 backend=OpenCL name=kqv_out-7 op=RESHAPE
[split-node] split=13 node=53 backend=OpenCL name=node_463 op=MUL_MAT
[split-node] split=13 node=54 backend=OpenCL name=ffn_inp-7 op=ADD
[split-node] split=13 node=55 backend=OpenCL name=norm-7 op=RMS_NORM
[split-node] split=13 node=56 backend=OpenCL name=ffn_norm-7 op=MUL
[split-node] split=13 node=57 backend=OpenCL name=ffn_moe_logits-7 op=MUL_MAT
[split-node] split=13 node=58 backend=OpenCL name=ffn_moe_probs-7 op=SOFT_MAX
[split-node] split=13 node=59 backend=OpenCL name=ffn_moe_probs-7 (reshaped) op=RESHAPE
[split-node] split=13 node=60 backend=OpenCL name=ffn_moe_argsort-7 op=ARGSORT
[split-node] split=13 node=61 backend=OpenCL name=ffn_moe_topk-7 op=VIEW
[split-node] split=13 node=62 backend=OpenCL name=ffn_moe_weights-7 op=GET_ROWS
[split-input] split=13 name=ffn_moe_weights_scaled-6 bytes=12288 backend_dst=OpenCL
[split-input] split=13 name=ffn_moe_topk-7 bytes=130840 backend_dst=OpenCL
[split-summary] id=14 backend=CPU nodes=2 inputs=1
[split-node] split=14 node=0 backend=CPU name=ffn_moe_weights_scaled-7 op=SCALE
[split-node] split=14 node=1 backend=OpenCL name=ffn_norm-7 (reshaped) op=RESHAPE
[split-input] split=14 name=ffn_moe_weights-7 bytes=12288 backend_dst=CPU
[split-summary] id=15 backend=OpenCL nodes=63 inputs=2
[split-node] split=15 node=0 backend=OpenCL name=ffn_moe_gate-7 op=MUL_MAT_ID
[split-node] split=15 node=1 backend=OpenCL name=ffn_moe_up-7 op=MUL_MAT_ID
[split-node] split=15 node=2 backend=OpenCL name=ffn_moe_weighted-7 op=(null)
[split-node] split=15 node=3 backend=OpenCL name=ffn_moe_down-7 op=MUL_MAT_ID
[split-node] split=15 node=4 backend=OpenCL name=node_479 op=MUL
[split-node] split=15 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=15 node=6 backend=OpenCL name=node_479 (view) op=VIEW
[split-node] split=15 node=7 backend=OpenCL name=node_479 (view) op=VIEW
[split-node] split=15 node=8 backend=OpenCL name=node_479 (view) op=VIEW
[split-node] split=15 node=9 backend=OpenCL name=node_479 (view) op=VIEW
[split-node] split=15 node=10 backend=OpenCL name=node_479 (view) op=VIEW
[split-node] split=15 node=11 backend=OpenCL name=ffn_gate-7 op=MUL_MAT
[split-node] split=15 node=12 backend=OpenCL name=ffn_up-7 op=MUL_MAT
[split-node] split=15 node=13 backend=OpenCL name=ffn_swiglu-7 op=(null)
[split-node] split=15 node=14 backend=OpenCL name=node_489 op=ADD
[split-node] split=15 node=15 backend=OpenCL name=node_490 op=ADD
[split-node] split=15 node=16 backend=OpenCL name=node_491 op=ADD
[split-node] split=15 node=17 backend=OpenCL name=node_492 op=ADD
[split-node] split=15 node=18 backend=OpenCL name=ffn_moe_out-7 op=ADD
[split-node] split=15 node=19 backend=OpenCL name=ffn_shexp-7 op=MUL_MAT
[split-node] split=15 node=20 backend=OpenCL name=ffn_out-7 op=ADD
[split-node] split=15 node=21 backend=OpenCL name=l_out-7 op=ADD
[split-node] split=15 node=22 backend=OpenCL name=norm-8 op=RMS_NORM
[split-node] split=15 node=23 backend=OpenCL name=attn_norm-8 op=MUL
[split-node] split=15 node=24 backend=OpenCL name=q-8 op=MUL_MAT
[split-node] split=15 node=25 backend=OpenCL name=q_pe-8 op=VIEW
[split-node] split=15 node=26 backend=OpenCL name=q_pe-8 op=ROPE
[split-node] split=15 node=27 backend=OpenCL name=q_nope-8 op=VIEW
[split-node] split=15 node=28 backend=OpenCL name=Qcur-8 op=CONCAT
[split-node] split=15 node=29 backend=OpenCL name=kv_cmpr_pe-8 op=MUL_MAT
[split-node] split=15 node=30 backend=OpenCL name=k_pe-8 op=VIEW
[split-node] split=15 node=31 backend=OpenCL name=k_pe-8 op=ROPE
[split-node] split=15 node=32 backend=OpenCL name=node_507 op=REPEAT
[split-node] split=15 node=33 backend=OpenCL name=kv_cmpr-8 op=VIEW
[split-node] split=15 node=34 backend=OpenCL name=norm-8 op=RMS_NORM
[split-node] split=15 node=35 backend=OpenCL name=kv_cmpr-8 op=MUL
[split-node] split=15 node=36 backend=OpenCL name=kv-8 op=MUL_MAT
[split-node] split=15 node=37 backend=OpenCL name=k_nope_view-8 op=VIEW
[split-node] split=15 node=38 backend=OpenCL name=Kcur-8 op=CONCAT
[split-node] split=15 node=39 backend=OpenCL name=Vcur_view-8 op=VIEW
[split-node] split=15 node=40 backend=OpenCL name=Vcur_cont-8 op=CONT
[split-node] split=15 node=41 backend=OpenCL name=Kcur-8 (view) op=VIEW
[split-node] split=15 node=42 backend=OpenCL name=cache_k_l8 (view) op=SET_ROWS
[split-node] split=15 node=43 backend=OpenCL name=Vcur_cont-8 (view) op=VIEW
[split-node] split=15 node=44 backend=OpenCL name=cache_v_l8 (view) op=SET_ROWS
[split-node] split=15 node=45 backend=OpenCL name=Qcur-8 (view) op=VIEW
[split-node] split=15 node=46 backend=OpenCL name=Qcur-8 (view) (permuted) op=PERMUTE
[split-node] split=15 node=47 backend=OpenCL name=cache_k_l8 (view) op=VIEW
[split-node] split=15 node=48 backend=OpenCL name=cache_k_l8 (view) (permuted) op=PERMUTE
[split-node] split=15 node=49 backend=OpenCL name=cache_v_l8 (view) op=VIEW
[split-node] split=15 node=50 backend=OpenCL name=cache_v_l8 (view) (permuted) op=PERMUTE
[split-node] split=15 node=51 backend=OpenCL name=__fattn__-8 op=FLASH_ATTN_BACK
[split-node] split=15 node=52 backend=OpenCL name=kqv_out-8 op=RESHAPE
[split-node] split=15 node=53 backend=OpenCL name=node_528 op=MUL_MAT
[split-node] split=15 node=54 backend=OpenCL name=ffn_inp-8 op=ADD
[split-node] split=15 node=55 backend=OpenCL name=norm-8 op=RMS_NORM
[split-node] split=15 node=56 backend=OpenCL name=ffn_norm-8 op=MUL
[split-node] split=15 node=57 backend=OpenCL name=ffn_moe_logits-8 op=MUL_MAT
[split-node] split=15 node=58 backend=OpenCL name=ffn_moe_probs-8 op=SOFT_MAX
[split-node] split=15 node=59 backend=OpenCL name=ffn_moe_probs-8 (reshaped) op=RESHAPE
[split-node] split=15 node=60 backend=OpenCL name=ffn_moe_argsort-8 op=ARGSORT
[split-node] split=15 node=61 backend=OpenCL name=ffn_moe_topk-8 op=VIEW
[split-node] split=15 node=62 backend=OpenCL name=ffn_moe_weights-8 op=GET_ROWS
[split-input] split=15 name=ffn_moe_weights_scaled-7 bytes=12288 backend_dst=OpenCL
[split-input] split=15 name=ffn_moe_topk-8 bytes=130840 backend_dst=OpenCL
[split-summary] id=16 backend=CPU nodes=2 inputs=1
[split-node] split=16 node=0 backend=CPU name=ffn_moe_weights_scaled-8 op=SCALE
[split-node] split=16 node=1 backend=OpenCL name=ffn_norm-8 (reshaped) op=RESHAPE
[split-input] split=16 name=ffn_moe_weights-8 bytes=12288 backend_dst=CPU
[split-summary] id=17 backend=OpenCL nodes=63 inputs=2
[split-node] split=17 node=0 backend=OpenCL name=ffn_moe_gate-8 op=MUL_MAT_ID
[split-node] split=17 node=1 backend=OpenCL name=ffn_moe_up-8 op=MUL_MAT_ID
[split-node] split=17 node=2 backend=OpenCL name=ffn_moe_weighted-8 op=(null)
[split-node] split=17 node=3 backend=OpenCL name=ffn_moe_down-8 op=MUL_MAT_ID
[split-node] split=17 node=4 backend=OpenCL name=node_544 op=MUL
[split-node] split=17 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=17 node=6 backend=OpenCL name=node_544 (view) op=VIEW
[split-node] split=17 node=7 backend=OpenCL name=node_544 (view) op=VIEW
[split-node] split=17 node=8 backend=OpenCL name=node_544 (view) op=VIEW
[split-node] split=17 node=9 backend=OpenCL name=node_544 (view) op=VIEW
[split-node] split=17 node=10 backend=OpenCL name=node_544 (view) op=VIEW
[split-node] split=17 node=11 backend=OpenCL name=ffn_gate-8 op=MUL_MAT
[split-node] split=17 node=12 backend=OpenCL name=ffn_up-8 op=MUL_MAT
[split-node] split=17 node=13 backend=OpenCL name=ffn_swiglu-8 op=(null)
[split-node] split=17 node=14 backend=OpenCL name=node_554 op=ADD
[split-node] split=17 node=15 backend=OpenCL name=node_555 op=ADD
[split-node] split=17 node=16 backend=OpenCL name=node_556 op=ADD
[split-node] split=17 node=17 backend=OpenCL name=node_557 op=ADD
[split-node] split=17 node=18 backend=OpenCL name=ffn_moe_out-8 op=ADD
[split-node] split=17 node=19 backend=OpenCL name=ffn_shexp-8 op=MUL_MAT
[split-node] split=17 node=20 backend=OpenCL name=ffn_out-8 op=ADD
[split-node] split=17 node=21 backend=OpenCL name=l_out-8 op=ADD
[split-node] split=17 node=22 backend=OpenCL name=norm-9 op=RMS_NORM
[split-node] split=17 node=23 backend=OpenCL name=attn_norm-9 op=MUL
[split-node] split=17 node=24 backend=OpenCL name=q-9 op=MUL_MAT
[split-node] split=17 node=25 backend=OpenCL name=q_pe-9 op=VIEW
[split-node] split=17 node=26 backend=OpenCL name=q_pe-9 op=ROPE
[split-node] split=17 node=27 backend=OpenCL name=q_nope-9 op=VIEW
[split-node] split=17 node=28 backend=OpenCL name=Qcur-9 op=CONCAT
[split-node] split=17 node=29 backend=OpenCL name=kv_cmpr_pe-9 op=MUL_MAT
[split-node] split=17 node=30 backend=OpenCL name=k_pe-9 op=VIEW
[split-node] split=17 node=31 backend=OpenCL name=k_pe-9 op=ROPE
[split-node] split=17 node=32 backend=OpenCL name=node_572 op=REPEAT
[split-node] split=17 node=33 backend=OpenCL name=kv_cmpr-9 op=VIEW
[split-node] split=17 node=34 backend=OpenCL name=norm-9 op=RMS_NORM
[split-node] split=17 node=35 backend=OpenCL name=kv_cmpr-9 op=MUL
[split-node] split=17 node=36 backend=OpenCL name=kv-9 op=MUL_MAT
[split-node] split=17 node=37 backend=OpenCL name=k_nope_view-9 op=VIEW
[split-node] split=17 node=38 backend=OpenCL name=Kcur-9 op=CONCAT
[split-node] split=17 node=39 backend=OpenCL name=Vcur_view-9 op=VIEW
[split-node] split=17 node=40 backend=OpenCL name=Vcur_cont-9 op=CONT
[split-node] split=17 node=41 backend=OpenCL name=Kcur-9 (view) op=VIEW
[split-node] split=17 node=42 backend=OpenCL name=cache_k_l9 (view) op=SET_ROWS
[split-node] split=17 node=43 backend=OpenCL name=Vcur_cont-9 (view) op=VIEW
[split-node] split=17 node=44 backend=OpenCL name=cache_v_l9 (view) op=SET_ROWS
[split-node] split=17 node=45 backend=OpenCL name=Qcur-9 (view) op=VIEW
[split-node] split=17 node=46 backend=OpenCL name=Qcur-9 (view) (permuted) op=PERMUTE
[split-node] split=17 node=47 backend=OpenCL name=cache_k_l9 (view) op=VIEW
[split-node] split=17 node=48 backend=OpenCL name=cache_k_l9 (view) (permuted) op=PERMUTE
[split-node] split=17 node=49 backend=OpenCL name=cache_v_l9 (view) op=VIEW
[split-node] split=17 node=50 backend=OpenCL name=cache_v_l9 (view) (permuted) op=PERMUTE
[split-node] split=17 node=51 backend=OpenCL name=__fattn__-9 op=FLASH_ATTN_BACK
[split-node] split=17 node=52 backend=OpenCL name=kqv_out-9 op=RESHAPE
[split-node] split=17 node=53 backend=OpenCL name=node_593 op=MUL_MAT
[split-node] split=17 node=54 backend=OpenCL name=ffn_inp-9 op=ADD
[split-node] split=17 node=55 backend=OpenCL name=norm-9 op=RMS_NORM
[split-node] split=17 node=56 backend=OpenCL name=ffn_norm-9 op=MUL
[split-node] split=17 node=57 backend=OpenCL name=ffn_moe_logits-9 op=MUL_MAT
[split-node] split=17 node=58 backend=OpenCL name=ffn_moe_probs-9 op=SOFT_MAX
[split-node] split=17 node=59 backend=OpenCL name=ffn_moe_probs-9 (reshaped) op=RESHAPE
[split-node] split=17 node=60 backend=OpenCL name=ffn_moe_argsort-9 op=ARGSORT
[split-node] split=17 node=61 backend=OpenCL name=ffn_moe_topk-9 op=VIEW
[split-node] split=17 node=62 backend=OpenCL name=ffn_moe_weights-9 op=GET_ROWS
[split-input] split=17 name=ffn_moe_weights_scaled-8 bytes=12288 backend_dst=OpenCL
[split-input] split=17 name=ffn_moe_topk-9 bytes=130840 backend_dst=OpenCL
[split-summary] id=18 backend=CPU nodes=2 inputs=1
[split-node] split=18 node=0 backend=CPU name=ffn_moe_weights_scaled-9 op=SCALE
[split-node] split=18 node=1 backend=OpenCL name=ffn_norm-9 (reshaped) op=RESHAPE
[split-input] split=18 name=ffn_moe_weights-9 bytes=12288 backend_dst=CPU
[split-summary] id=19 backend=OpenCL nodes=63 inputs=2
[split-node] split=19 node=0 backend=OpenCL name=ffn_moe_gate-9 op=MUL_MAT_ID
[split-node] split=19 node=1 backend=OpenCL name=ffn_moe_up-9 op=MUL_MAT_ID
[split-node] split=19 node=2 backend=OpenCL name=ffn_moe_weighted-9 op=(null)
[split-node] split=19 node=3 backend=OpenCL name=ffn_moe_down-9 op=MUL_MAT_ID
[split-node] split=19 node=4 backend=OpenCL name=node_609 op=MUL
[split-node] split=19 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=19 node=6 backend=OpenCL name=node_609 (view) op=VIEW
[split-node] split=19 node=7 backend=OpenCL name=node_609 (view) op=VIEW
[split-node] split=19 node=8 backend=OpenCL name=node_609 (view) op=VIEW
[split-node] split=19 node=9 backend=OpenCL name=node_609 (view) op=VIEW
[split-node] split=19 node=10 backend=OpenCL name=node_609 (view) op=VIEW
[split-node] split=19 node=11 backend=OpenCL name=ffn_gate-9 op=MUL_MAT
[split-node] split=19 node=12 backend=OpenCL name=ffn_up-9 op=MUL_MAT
[split-node] split=19 node=13 backend=OpenCL name=ffn_swiglu-9 op=(null)
[split-node] split=19 node=14 backend=OpenCL name=node_619 op=ADD
[split-node] split=19 node=15 backend=OpenCL name=node_620 op=ADD
[split-node] split=19 node=16 backend=OpenCL name=node_621 op=ADD
[split-node] split=19 node=17 backend=OpenCL name=node_622 op=ADD
[split-node] split=19 node=18 backend=OpenCL name=ffn_moe_out-9 op=ADD
[split-node] split=19 node=19 backend=OpenCL name=ffn_shexp-9 op=MUL_MAT
[split-node] split=19 node=20 backend=OpenCL name=ffn_out-9 op=ADD
[split-node] split=19 node=21 backend=OpenCL name=l_out-9 op=ADD
[split-node] split=19 node=22 backend=OpenCL name=norm-10 op=RMS_NORM
[split-node] split=19 node=23 backend=OpenCL name=attn_norm-10 op=MUL
[split-node] split=19 node=24 backend=OpenCL name=q-10 op=MUL_MAT
[split-node] split=19 node=25 backend=OpenCL name=q_pe-10 op=VIEW
[split-node] split=19 node=26 backend=OpenCL name=q_pe-10 op=ROPE
[split-node] split=19 node=27 backend=OpenCL name=q_nope-10 op=VIEW
[split-node] split=19 node=28 backend=OpenCL name=Qcur-10 op=CONCAT
[split-node] split=19 node=29 backend=OpenCL name=kv_cmpr_pe-10 op=MUL_MAT
[split-node] split=19 node=30 backend=OpenCL name=k_pe-10 op=VIEW
[split-node] split=19 node=31 backend=OpenCL name=k_pe-10 op=ROPE
[split-node] split=19 node=32 backend=OpenCL name=node_637 op=REPEAT
[split-node] split=19 node=33 backend=OpenCL name=kv_cmpr-10 op=VIEW
[split-node] split=19 node=34 backend=OpenCL name=norm-10 op=RMS_NORM
[split-node] split=19 node=35 backend=OpenCL name=kv_cmpr-10 op=MUL
[split-node] split=19 node=36 backend=OpenCL name=kv-10 op=MUL_MAT
[split-node] split=19 node=37 backend=OpenCL name=k_nope_view-10 op=VIEW
[split-node] split=19 node=38 backend=OpenCL name=Kcur-10 op=CONCAT
[split-node] split=19 node=39 backend=OpenCL name=Vcur_view-10 op=VIEW
[split-node] split=19 node=40 backend=OpenCL name=Vcur_cont-10 op=CONT
[split-node] split=19 node=41 backend=OpenCL name=Kcur-10 (view) op=VIEW
[split-node] split=19 node=42 backend=OpenCL name=cache_k_l10 (view) op=SET_ROWS
[split-node] split=19 node=43 backend=OpenCL name=Vcur_cont-10 (view) op=VIEW
[split-node] split=19 node=44 backend=OpenCL name=cache_v_l10 (view) op=SET_ROWS
[split-node] split=19 node=45 backend=OpenCL name=Qcur-10 (view) op=VIEW
[split-node] split=19 node=46 backend=OpenCL name=Qcur-10 (view) (permuted) op=PERMUTE
[split-node] split=19 node=47 backend=OpenCL name=cache_k_l10 (view) op=VIEW
[split-node] split=19 node=48 backend=OpenCL name=cache_k_l10 (view) (permuted) op=PERMUTE
[split-node] split=19 node=49 backend=OpenCL name=cache_v_l10 (view) op=VIEW
[split-node] split=19 node=50 backend=OpenCL name=cache_v_l10 (view) (permuted) op=PERMUTE
[split-node] split=19 node=51 backend=OpenCL name=__fattn__-10 op=FLASH_ATTN_BACK
[split-node] split=19 node=52 backend=OpenCL name=kqv_out-10 op=RESHAPE
[split-node] split=19 node=53 backend=OpenCL name=node_658 op=MUL_MAT
[split-node] split=19 node=54 backend=OpenCL name=ffn_inp-10 op=ADD
[split-node] split=19 node=55 backend=OpenCL name=norm-10 op=RMS_NORM
[split-node] split=19 node=56 backend=OpenCL name=ffn_norm-10 op=MUL
[split-node] split=19 node=57 backend=OpenCL name=ffn_moe_logits-10 op=MUL_MAT
[split-node] split=19 node=58 backend=OpenCL name=ffn_moe_probs-10 op=SOFT_MAX
[split-node] split=19 node=59 backend=OpenCL name=ffn_moe_probs-10 (reshaped) op=RESHAPE
[split-node] split=19 node=60 backend=OpenCL name=ffn_moe_argsort-10 op=ARGSORT
[split-node] split=19 node=61 backend=OpenCL name=ffn_moe_topk-10 op=VIEW
[split-node] split=19 node=62 backend=OpenCL name=ffn_moe_weights-10 op=GET_ROWS
[split-input] split=19 name=ffn_moe_weights_scaled-9 bytes=12288 backend_dst=OpenCL
[split-input] split=19 name=ffn_moe_topk-10 bytes=130840 backend_dst=OpenCL
[split-summary] id=20 backend=CPU nodes=2 inputs=1
[split-node] split=20 node=0 backend=CPU name=ffn_moe_weights_scaled-10 op=SCALE
[split-node] split=20 node=1 backend=OpenCL name=ffn_norm-10 (reshaped) op=RESHAPE
[split-input] split=20 name=ffn_moe_weights-10 bytes=12288 backend_dst=CPU
[split-summary] id=21 backend=OpenCL nodes=63 inputs=2
[split-node] split=21 node=0 backend=OpenCL name=ffn_moe_gate-10 op=MUL_MAT_ID
[split-node] split=21 node=1 backend=OpenCL name=ffn_moe_up-10 op=MUL_MAT_ID
[split-node] split=21 node=2 backend=OpenCL name=ffn_moe_weighted-10 op=(null)
[split-node] split=21 node=3 backend=OpenCL name=ffn_moe_down-10 op=MUL_MAT_ID
[split-node] split=21 node=4 backend=OpenCL name=node_674 op=MUL
[split-node] split=21 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=21 node=6 backend=OpenCL name=node_674 (view) op=VIEW
[split-node] split=21 node=7 backend=OpenCL name=node_674 (view) op=VIEW
[split-node] split=21 node=8 backend=OpenCL name=node_674 (view) op=VIEW
[split-node] split=21 node=9 backend=OpenCL name=node_674 (view) op=VIEW
[split-node] split=21 node=10 backend=OpenCL name=node_674 (view) op=VIEW
[split-node] split=21 node=11 backend=OpenCL name=ffn_gate-10 op=MUL_MAT
[split-node] split=21 node=12 backend=OpenCL name=ffn_up-10 op=MUL_MAT
[split-node] split=21 node=13 backend=OpenCL name=ffn_swiglu-10 op=(null)
[split-node] split=21 node=14 backend=OpenCL name=node_684 op=ADD
[split-node] split=21 node=15 backend=OpenCL name=node_685 op=ADD
[split-node] split=21 node=16 backend=OpenCL name=node_686 op=ADD
[split-node] split=21 node=17 backend=OpenCL name=node_687 op=ADD
[split-node] split=21 node=18 backend=OpenCL name=ffn_moe_out-10 op=ADD
[split-node] split=21 node=19 backend=OpenCL name=ffn_shexp-10 op=MUL_MAT
[split-node] split=21 node=20 backend=OpenCL name=ffn_out-10 op=ADD
[split-node] split=21 node=21 backend=OpenCL name=l_out-10 op=ADD
[split-node] split=21 node=22 backend=OpenCL name=norm-11 op=RMS_NORM
[split-node] split=21 node=23 backend=OpenCL name=attn_norm-11 op=MUL
[split-node] split=21 node=24 backend=OpenCL name=q-11 op=MUL_MAT
[split-node] split=21 node=25 backend=OpenCL name=q_pe-11 op=VIEW
[split-node] split=21 node=26 backend=OpenCL name=q_pe-11 op=ROPE
[split-node] split=21 node=27 backend=OpenCL name=q_nope-11 op=VIEW
[split-node] split=21 node=28 backend=OpenCL name=Qcur-11 op=CONCAT
[split-node] split=21 node=29 backend=OpenCL name=kv_cmpr_pe-11 op=MUL_MAT
[split-node] split=21 node=30 backend=OpenCL name=k_pe-11 op=VIEW
[split-node] split=21 node=31 backend=OpenCL name=k_pe-11 op=ROPE
[split-node] split=21 node=32 backend=OpenCL name=node_702 op=REPEAT
[split-node] split=21 node=33 backend=OpenCL name=kv_cmpr-11 op=VIEW
[split-node] split=21 node=34 backend=OpenCL name=norm-11 op=RMS_NORM
[split-node] split=21 node=35 backend=OpenCL name=kv_cmpr-11 op=MUL
[split-node] split=21 node=36 backend=OpenCL name=kv-11 op=MUL_MAT
[split-node] split=21 node=37 backend=OpenCL name=k_nope_view-11 op=VIEW
[split-node] split=21 node=38 backend=OpenCL name=Kcur-11 op=CONCAT
[split-node] split=21 node=39 backend=OpenCL name=Vcur_view-11 op=VIEW
[split-node] split=21 node=40 backend=OpenCL name=Vcur_cont-11 op=CONT
[split-node] split=21 node=41 backend=OpenCL name=Kcur-11 (view) op=VIEW
[split-node] split=21 node=42 backend=OpenCL name=cache_k_l11 (view) op=SET_ROWS
[split-node] split=21 node=43 backend=OpenCL name=Vcur_cont-11 (view) op=VIEW
[split-node] split=21 node=44 backend=OpenCL name=cache_v_l11 (view) op=SET_ROWS
[split-node] split=21 node=45 backend=OpenCL name=Qcur-11 (view) op=VIEW
[split-node] split=21 node=46 backend=OpenCL name=Qcur-11 (view) (permuted) op=PERMUTE
[split-node] split=21 node=47 backend=OpenCL name=cache_k_l11 (view) op=VIEW
[split-node] split=21 node=48 backend=OpenCL name=cache_k_l11 (view) (permuted) op=PERMUTE
[split-node] split=21 node=49 backend=OpenCL name=cache_v_l11 (view) op=VIEW
[split-node] split=21 node=50 backend=OpenCL name=cache_v_l11 (view) (permuted) op=PERMUTE
[split-node] split=21 node=51 backend=OpenCL name=__fattn__-11 op=FLASH_ATTN_BACK
[split-node] split=21 node=52 backend=OpenCL name=kqv_out-11 op=RESHAPE
[split-node] split=21 node=53 backend=OpenCL name=node_723 op=MUL_MAT
[split-node] split=21 node=54 backend=OpenCL name=ffn_inp-11 op=ADD
[split-node] split=21 node=55 backend=OpenCL name=norm-11 op=RMS_NORM
[split-node] split=21 node=56 backend=OpenCL name=ffn_norm-11 op=MUL
[split-node] split=21 node=57 backend=OpenCL name=ffn_moe_logits-11 op=MUL_MAT
[split-node] split=21 node=58 backend=OpenCL name=ffn_moe_probs-11 op=SOFT_MAX
[split-node] split=21 node=59 backend=OpenCL name=ffn_moe_probs-11 (reshaped) op=RESHAPE
[split-node] split=21 node=60 backend=OpenCL name=ffn_moe_argsort-11 op=ARGSORT
[split-node] split=21 node=61 backend=OpenCL name=ffn_moe_topk-11 op=VIEW
[split-node] split=21 node=62 backend=OpenCL name=ffn_moe_weights-11 op=GET_ROWS
[split-input] split=21 name=ffn_moe_weights_scaled-10 bytes=12288 backend_dst=OpenCL
[split-input] split=21 name=ffn_moe_topk-11 bytes=130840 backend_dst=OpenCL
[split-summary] id=22 backend=CPU nodes=2 inputs=1
[split-node] split=22 node=0 backend=CPU name=ffn_moe_weights_scaled-11 op=SCALE
[split-node] split=22 node=1 backend=OpenCL name=ffn_norm-11 (reshaped) op=RESHAPE
[split-input] split=22 name=ffn_moe_weights-11 bytes=12288 backend_dst=CPU
[split-summary] id=23 backend=OpenCL nodes=63 inputs=2
[split-node] split=23 node=0 backend=OpenCL name=ffn_moe_gate-11 op=MUL_MAT_ID
[split-node] split=23 node=1 backend=OpenCL name=ffn_moe_up-11 op=MUL_MAT_ID
[split-node] split=23 node=2 backend=OpenCL name=ffn_moe_weighted-11 op=(null)
[split-node] split=23 node=3 backend=OpenCL name=ffn_moe_down-11 op=MUL_MAT_ID
[split-node] split=23 node=4 backend=OpenCL name=node_739 op=MUL
[split-node] split=23 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=23 node=6 backend=OpenCL name=node_739 (view) op=VIEW
[split-node] split=23 node=7 backend=OpenCL name=node_739 (view) op=VIEW
[split-node] split=23 node=8 backend=OpenCL name=node_739 (view) op=VIEW
[split-node] split=23 node=9 backend=OpenCL name=node_739 (view) op=VIEW
[split-node] split=23 node=10 backend=OpenCL name=node_739 (view) op=VIEW
[split-node] split=23 node=11 backend=OpenCL name=ffn_gate-11 op=MUL_MAT
[split-node] split=23 node=12 backend=OpenCL name=ffn_up-11 op=MUL_MAT
[split-node] split=23 node=13 backend=OpenCL name=ffn_swiglu-11 op=(null)
[split-node] split=23 node=14 backend=OpenCL name=node_749 op=ADD
[split-node] split=23 node=15 backend=OpenCL name=node_750 op=ADD
[split-node] split=23 node=16 backend=OpenCL name=node_751 op=ADD
[split-node] split=23 node=17 backend=OpenCL name=node_752 op=ADD
[split-node] split=23 node=18 backend=OpenCL name=ffn_moe_out-11 op=ADD
[split-node] split=23 node=19 backend=OpenCL name=ffn_shexp-11 op=MUL_MAT
[split-node] split=23 node=20 backend=OpenCL name=ffn_out-11 op=ADD
[split-node] split=23 node=21 backend=OpenCL name=l_out-11 op=ADD
[split-node] split=23 node=22 backend=OpenCL name=norm-12 op=RMS_NORM
[split-node] split=23 node=23 backend=OpenCL name=attn_norm-12 op=MUL
[split-node] split=23 node=24 backend=OpenCL name=q-12 op=MUL_MAT
[split-node] split=23 node=25 backend=OpenCL name=q_pe-12 op=VIEW
[split-node] split=23 node=26 backend=OpenCL name=q_pe-12 op=ROPE
[split-node] split=23 node=27 backend=OpenCL name=q_nope-12 op=VIEW
[split-node] split=23 node=28 backend=OpenCL name=Qcur-12 op=CONCAT
[split-node] split=23 node=29 backend=OpenCL name=kv_cmpr_pe-12 op=MUL_MAT
[split-node] split=23 node=30 backend=OpenCL name=k_pe-12 op=VIEW
[split-node] split=23 node=31 backend=OpenCL name=k_pe-12 op=ROPE
[split-node] split=23 node=32 backend=OpenCL name=node_767 op=REPEAT
[split-node] split=23 node=33 backend=OpenCL name=kv_cmpr-12 op=VIEW
[split-node] split=23 node=34 backend=OpenCL name=norm-12 op=RMS_NORM
[split-node] split=23 node=35 backend=OpenCL name=kv_cmpr-12 op=MUL
[split-node] split=23 node=36 backend=OpenCL name=kv-12 op=MUL_MAT
[split-node] split=23 node=37 backend=OpenCL name=k_nope_view-12 op=VIEW
[split-node] split=23 node=38 backend=OpenCL name=Kcur-12 op=CONCAT
[split-node] split=23 node=39 backend=OpenCL name=Vcur_view-12 op=VIEW
[split-node] split=23 node=40 backend=OpenCL name=Vcur_cont-12 op=CONT
[split-node] split=23 node=41 backend=OpenCL name=Kcur-12 (view) op=VIEW
[split-node] split=23 node=42 backend=OpenCL name=cache_k_l12 (view) op=SET_ROWS
[split-node] split=23 node=43 backend=OpenCL name=Vcur_cont-12 (view) op=VIEW
[split-node] split=23 node=44 backend=OpenCL name=cache_v_l12 (view) op=SET_ROWS
[split-node] split=23 node=45 backend=OpenCL name=Qcur-12 (view) op=VIEW
[split-node] split=23 node=46 backend=OpenCL name=Qcur-12 (view) (permuted) op=PERMUTE
[split-node] split=23 node=47 backend=OpenCL name=cache_k_l12 (view) op=VIEW
[split-node] split=23 node=48 backend=OpenCL name=cache_k_l12 (view) (permuted) op=PERMUTE
[split-node] split=23 node=49 backend=OpenCL name=cache_v_l12 (view) op=VIEW
[split-node] split=23 node=50 backend=OpenCL name=cache_v_l12 (view) (permuted) op=PERMUTE
[split-node] split=23 node=51 backend=OpenCL name=__fattn__-12 op=FLASH_ATTN_BACK
[split-node] split=23 node=52 backend=OpenCL name=kqv_out-12 op=RESHAPE
[split-node] split=23 node=53 backend=OpenCL name=node_788 op=MUL_MAT
[split-node] split=23 node=54 backend=OpenCL name=ffn_inp-12 op=ADD
[split-node] split=23 node=55 backend=OpenCL name=norm-12 op=RMS_NORM
[split-node] split=23 node=56 backend=OpenCL name=ffn_norm-12 op=MUL
[split-node] split=23 node=57 backend=OpenCL name=ffn_moe_logits-12 op=MUL_MAT
[split-node] split=23 node=58 backend=OpenCL name=ffn_moe_probs-12 op=SOFT_MAX
[split-node] split=23 node=59 backend=OpenCL name=ffn_moe_probs-12 (reshaped) op=RESHAPE
[split-node] split=23 node=60 backend=OpenCL name=ffn_moe_argsort-12 op=ARGSORT
[split-node] split=23 node=61 backend=OpenCL name=ffn_moe_topk-12 op=VIEW
[split-node] split=23 node=62 backend=OpenCL name=ffn_moe_weights-12 op=GET_ROWS
[split-input] split=23 name=ffn_moe_weights_scaled-11 bytes=12288 backend_dst=OpenCL
[split-input] split=23 name=ffn_moe_topk-12 bytes=130840 backend_dst=OpenCL
[split-summary] id=24 backend=CPU nodes=2 inputs=1
[split-node] split=24 node=0 backend=CPU name=ffn_moe_weights_scaled-12 op=SCALE
[split-node] split=24 node=1 backend=OpenCL name=ffn_norm-12 (reshaped) op=RESHAPE
[split-input] split=24 name=ffn_moe_weights-12 bytes=12288 backend_dst=CPU
[split-summary] id=25 backend=OpenCL nodes=63 inputs=2
[split-node] split=25 node=0 backend=OpenCL name=ffn_moe_gate-12 op=MUL_MAT_ID
[split-node] split=25 node=1 backend=OpenCL name=ffn_moe_up-12 op=MUL_MAT_ID
[split-node] split=25 node=2 backend=OpenCL name=ffn_moe_weighted-12 op=(null)
[split-node] split=25 node=3 backend=OpenCL name=ffn_moe_down-12 op=MUL_MAT_ID
[split-node] split=25 node=4 backend=OpenCL name=node_804 op=MUL
[split-node] split=25 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=25 node=6 backend=OpenCL name=node_804 (view) op=VIEW
[split-node] split=25 node=7 backend=OpenCL name=node_804 (view) op=VIEW
[split-node] split=25 node=8 backend=OpenCL name=node_804 (view) op=VIEW
[split-node] split=25 node=9 backend=OpenCL name=node_804 (view) op=VIEW
[split-node] split=25 node=10 backend=OpenCL name=node_804 (view) op=VIEW
[split-node] split=25 node=11 backend=OpenCL name=ffn_gate-12 op=MUL_MAT
[split-node] split=25 node=12 backend=OpenCL name=ffn_up-12 op=MUL_MAT
[split-node] split=25 node=13 backend=OpenCL name=ffn_swiglu-12 op=(null)
[split-node] split=25 node=14 backend=OpenCL name=node_814 op=ADD
[split-node] split=25 node=15 backend=OpenCL name=node_815 op=ADD
[split-node] split=25 node=16 backend=OpenCL name=node_816 op=ADD
[split-node] split=25 node=17 backend=OpenCL name=node_817 op=ADD
[split-node] split=25 node=18 backend=OpenCL name=ffn_moe_out-12 op=ADD
[split-node] split=25 node=19 backend=OpenCL name=ffn_shexp-12 op=MUL_MAT
[split-node] split=25 node=20 backend=OpenCL name=ffn_out-12 op=ADD
[split-node] split=25 node=21 backend=OpenCL name=l_out-12 op=ADD
[split-node] split=25 node=22 backend=OpenCL name=norm-13 op=RMS_NORM
[split-node] split=25 node=23 backend=OpenCL name=attn_norm-13 op=MUL
[split-node] split=25 node=24 backend=OpenCL name=q-13 op=MUL_MAT
[split-node] split=25 node=25 backend=OpenCL name=q_pe-13 op=VIEW
[split-node] split=25 node=26 backend=OpenCL name=q_pe-13 op=ROPE
[split-node] split=25 node=27 backend=OpenCL name=q_nope-13 op=VIEW
[split-node] split=25 node=28 backend=OpenCL name=Qcur-13 op=CONCAT
[split-node] split=25 node=29 backend=OpenCL name=kv_cmpr_pe-13 op=MUL_MAT
[split-node] split=25 node=30 backend=OpenCL name=k_pe-13 op=VIEW
[split-node] split=25 node=31 backend=OpenCL name=k_pe-13 op=ROPE
[split-node] split=25 node=32 backend=OpenCL name=node_832 op=REPEAT
[split-node] split=25 node=33 backend=OpenCL name=kv_cmpr-13 op=VIEW
[split-node] split=25 node=34 backend=OpenCL name=norm-13 op=RMS_NORM
[split-node] split=25 node=35 backend=OpenCL name=kv_cmpr-13 op=MUL
[split-node] split=25 node=36 backend=OpenCL name=kv-13 op=MUL_MAT
[split-node] split=25 node=37 backend=OpenCL name=k_nope_view-13 op=VIEW
[split-node] split=25 node=38 backend=OpenCL name=Kcur-13 op=CONCAT
[split-node] split=25 node=39 backend=OpenCL name=Vcur_view-13 op=VIEW
[split-node] split=25 node=40 backend=OpenCL name=Vcur_cont-13 op=CONT
[split-node] split=25 node=41 backend=OpenCL name=Kcur-13 (view) op=VIEW
[split-node] split=25 node=42 backend=OpenCL name=cache_k_l13 (view) op=SET_ROWS
[split-node] split=25 node=43 backend=OpenCL name=Vcur_cont-13 (view) op=VIEW
[split-node] split=25 node=44 backend=OpenCL name=cache_v_l13 (view) op=SET_ROWS
[split-node] split=25 node=45 backend=OpenCL name=Qcur-13 (view) op=VIEW
[split-node] split=25 node=46 backend=OpenCL name=Qcur-13 (view) (permuted) op=PERMUTE
[split-node] split=25 node=47 backend=OpenCL name=cache_k_l13 (view) op=VIEW
[split-node] split=25 node=48 backend=OpenCL name=cache_k_l13 (view) (permuted) op=PERMUTE
[split-node] split=25 node=49 backend=OpenCL name=cache_v_l13 (view) op=VIEW
[split-node] split=25 node=50 backend=OpenCL name=cache_v_l13 (view) (permuted) op=PERMUTE
[split-node] split=25 node=51 backend=OpenCL name=__fattn__-13 op=FLASH_ATTN_BACK
[split-node] split=25 node=52 backend=OpenCL name=kqv_out-13 op=RESHAPE
[split-node] split=25 node=53 backend=OpenCL name=node_853 op=MUL_MAT
[split-node] split=25 node=54 backend=OpenCL name=ffn_inp-13 op=ADD
[split-node] split=25 node=55 backend=OpenCL name=norm-13 op=RMS_NORM
[split-node] split=25 node=56 backend=OpenCL name=ffn_norm-13 op=MUL
[split-node] split=25 node=57 backend=OpenCL name=ffn_moe_logits-13 op=MUL_MAT
[split-node] split=25 node=58 backend=OpenCL name=ffn_moe_probs-13 op=SOFT_MAX
[split-node] split=25 node=59 backend=OpenCL name=ffn_moe_probs-13 (reshaped) op=RESHAPE
[split-node] split=25 node=60 backend=OpenCL name=ffn_moe_argsort-13 op=ARGSORT
[split-node] split=25 node=61 backend=OpenCL name=ffn_moe_topk-13 op=VIEW
[split-node] split=25 node=62 backend=OpenCL name=ffn_moe_weights-13 op=GET_ROWS
[split-input] split=25 name=ffn_moe_weights_scaled-12 bytes=12288 backend_dst=OpenCL
[split-input] split=25 name=ffn_moe_topk-13 bytes=130840 backend_dst=OpenCL
[split-summary] id=26 backend=CPU nodes=2 inputs=1
[split-node] split=26 node=0 backend=CPU name=ffn_moe_weights_scaled-13 op=SCALE
[split-node] split=26 node=1 backend=OpenCL name=ffn_norm-13 (reshaped) op=RESHAPE
[split-input] split=26 name=ffn_moe_weights-13 bytes=12288 backend_dst=CPU
[split-summary] id=27 backend=OpenCL nodes=63 inputs=2
[split-node] split=27 node=0 backend=OpenCL name=ffn_moe_gate-13 op=MUL_MAT_ID
[split-node] split=27 node=1 backend=OpenCL name=ffn_moe_up-13 op=MUL_MAT_ID
[split-node] split=27 node=2 backend=OpenCL name=ffn_moe_weighted-13 op=(null)
[split-node] split=27 node=3 backend=OpenCL name=ffn_moe_down-13 op=MUL_MAT_ID
[split-node] split=27 node=4 backend=OpenCL name=node_869 op=MUL
[split-node] split=27 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=27 node=6 backend=OpenCL name=node_869 (view) op=VIEW
[split-node] split=27 node=7 backend=OpenCL name=node_869 (view) op=VIEW
[split-node] split=27 node=8 backend=OpenCL name=node_869 (view) op=VIEW
[split-node] split=27 node=9 backend=OpenCL name=node_869 (view) op=VIEW
[split-node] split=27 node=10 backend=OpenCL name=node_869 (view) op=VIEW
[split-node] split=27 node=11 backend=OpenCL name=ffn_gate-13 op=MUL_MAT
[split-node] split=27 node=12 backend=OpenCL name=ffn_up-13 op=MUL_MAT
[split-node] split=27 node=13 backend=OpenCL name=ffn_swiglu-13 op=(null)
[split-node] split=27 node=14 backend=OpenCL name=node_879 op=ADD
[split-node] split=27 node=15 backend=OpenCL name=node_880 op=ADD
[split-node] split=27 node=16 backend=OpenCL name=node_881 op=ADD
[split-node] split=27 node=17 backend=OpenCL name=node_882 op=ADD
[split-node] split=27 node=18 backend=OpenCL name=ffn_moe_out-13 op=ADD
[split-node] split=27 node=19 backend=OpenCL name=ffn_shexp-13 op=MUL_MAT
[split-node] split=27 node=20 backend=OpenCL name=ffn_out-13 op=ADD
[split-node] split=27 node=21 backend=OpenCL name=l_out-13 op=ADD
[split-node] split=27 node=22 backend=OpenCL name=norm-14 op=RMS_NORM
[split-node] split=27 node=23 backend=OpenCL name=attn_norm-14 op=MUL
[split-node] split=27 node=24 backend=OpenCL name=q-14 op=MUL_MAT
[split-node] split=27 node=25 backend=OpenCL name=q_pe-14 op=VIEW
[split-node] split=27 node=26 backend=OpenCL name=q_pe-14 op=ROPE
[split-node] split=27 node=27 backend=OpenCL name=q_nope-14 op=VIEW
[split-node] split=27 node=28 backend=OpenCL name=Qcur-14 op=CONCAT
[split-node] split=27 node=29 backend=OpenCL name=kv_cmpr_pe-14 op=MUL_MAT
[split-node] split=27 node=30 backend=OpenCL name=k_pe-14 op=VIEW
[split-node] split=27 node=31 backend=OpenCL name=k_pe-14 op=ROPE
[split-node] split=27 node=32 backend=OpenCL name=node_897 op=REPEAT
[split-node] split=27 node=33 backend=OpenCL name=kv_cmpr-14 op=VIEW
[split-node] split=27 node=34 backend=OpenCL name=norm-14 op=RMS_NORM
[split-node] split=27 node=35 backend=OpenCL name=kv_cmpr-14 op=MUL
[split-node] split=27 node=36 backend=OpenCL name=kv-14 op=MUL_MAT
[split-node] split=27 node=37 backend=OpenCL name=k_nope_view-14 op=VIEW
[split-node] split=27 node=38 backend=OpenCL name=Kcur-14 op=CONCAT
[split-node] split=27 node=39 backend=OpenCL name=Vcur_view-14 op=VIEW
[split-node] split=27 node=40 backend=OpenCL name=Vcur_cont-14 op=CONT
[split-node] split=27 node=41 backend=OpenCL name=Kcur-14 (view) op=VIEW
[split-node] split=27 node=42 backend=OpenCL name=cache_k_l14 (view) op=SET_ROWS
[split-node] split=27 node=43 backend=OpenCL name=Vcur_cont-14 (view) op=VIEW
[split-node] split=27 node=44 backend=OpenCL name=cache_v_l14 (view) op=SET_ROWS
[split-node] split=27 node=45 backend=OpenCL name=Qcur-14 (view) op=VIEW
[split-node] split=27 node=46 backend=OpenCL name=Qcur-14 (view) (permuted) op=PERMUTE
[split-node] split=27 node=47 backend=OpenCL name=cache_k_l14 (view) op=VIEW
[split-node] split=27 node=48 backend=OpenCL name=cache_k_l14 (view) (permuted) op=PERMUTE
[split-node] split=27 node=49 backend=OpenCL name=cache_v_l14 (view) op=VIEW
[split-node] split=27 node=50 backend=OpenCL name=cache_v_l14 (view) (permuted) op=PERMUTE
[split-node] split=27 node=51 backend=OpenCL name=__fattn__-14 op=FLASH_ATTN_BACK
[split-node] split=27 node=52 backend=OpenCL name=kqv_out-14 op=RESHAPE
[split-node] split=27 node=53 backend=OpenCL name=node_918 op=MUL_MAT
[split-node] split=27 node=54 backend=OpenCL name=ffn_inp-14 op=ADD
[split-node] split=27 node=55 backend=OpenCL name=norm-14 op=RMS_NORM
[split-node] split=27 node=56 backend=OpenCL name=ffn_norm-14 op=MUL
[split-node] split=27 node=57 backend=OpenCL name=ffn_moe_logits-14 op=MUL_MAT
[split-node] split=27 node=58 backend=OpenCL name=ffn_moe_probs-14 op=SOFT_MAX
[split-node] split=27 node=59 backend=OpenCL name=ffn_moe_probs-14 (reshaped) op=RESHAPE
[split-node] split=27 node=60 backend=OpenCL name=ffn_moe_argsort-14 op=ARGSORT
[split-node] split=27 node=61 backend=OpenCL name=ffn_moe_topk-14 op=VIEW
[split-node] split=27 node=62 backend=OpenCL name=ffn_moe_weights-14 op=GET_ROWS
[split-input] split=27 name=ffn_moe_weights_scaled-13 bytes=12288 backend_dst=OpenCL
[split-input] split=27 name=ffn_moe_topk-14 bytes=130840 backend_dst=OpenCL
[split-summary] id=28 backend=CPU nodes=2 inputs=1
[split-node] split=28 node=0 backend=CPU name=ffn_moe_weights_scaled-14 op=SCALE
[split-node] split=28 node=1 backend=OpenCL name=ffn_norm-14 (reshaped) op=RESHAPE
[split-input] split=28 name=ffn_moe_weights-14 bytes=12288 backend_dst=CPU
[split-summary] id=29 backend=OpenCL nodes=63 inputs=2
[split-node] split=29 node=0 backend=OpenCL name=ffn_moe_gate-14 op=MUL_MAT_ID
[split-node] split=29 node=1 backend=OpenCL name=ffn_moe_up-14 op=MUL_MAT_ID
[split-node] split=29 node=2 backend=OpenCL name=ffn_moe_weighted-14 op=(null)
[split-node] split=29 node=3 backend=OpenCL name=ffn_moe_down-14 op=MUL_MAT_ID
[split-node] split=29 node=4 backend=OpenCL name=node_934 op=MUL
[split-node] split=29 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=29 node=6 backend=OpenCL name=node_934 (view) op=VIEW
[split-node] split=29 node=7 backend=OpenCL name=node_934 (view) op=VIEW
[split-node] split=29 node=8 backend=OpenCL name=node_934 (view) op=VIEW
[split-node] split=29 node=9 backend=OpenCL name=node_934 (view) op=VIEW
[split-node] split=29 node=10 backend=OpenCL name=node_934 (view) op=VIEW
[split-node] split=29 node=11 backend=OpenCL name=ffn_gate-14 op=MUL_MAT
[split-node] split=29 node=12 backend=OpenCL name=ffn_up-14 op=MUL_MAT
[split-node] split=29 node=13 backend=OpenCL name=ffn_swiglu-14 op=(null)
[split-node] split=29 node=14 backend=OpenCL name=node_944 op=ADD
[split-node] split=29 node=15 backend=OpenCL name=node_945 op=ADD
[split-node] split=29 node=16 backend=OpenCL name=node_946 op=ADD
[split-node] split=29 node=17 backend=OpenCL name=node_947 op=ADD
[split-node] split=29 node=18 backend=OpenCL name=ffn_moe_out-14 op=ADD
[split-node] split=29 node=19 backend=OpenCL name=ffn_shexp-14 op=MUL_MAT
[split-node] split=29 node=20 backend=OpenCL name=ffn_out-14 op=ADD
[split-node] split=29 node=21 backend=OpenCL name=l_out-14 op=ADD
[split-node] split=29 node=22 backend=OpenCL name=norm-15 op=RMS_NORM
[split-node] split=29 node=23 backend=OpenCL name=attn_norm-15 op=MUL
[split-node] split=29 node=24 backend=OpenCL name=q-15 op=MUL_MAT
[split-node] split=29 node=25 backend=OpenCL name=q_pe-15 op=VIEW
[split-node] split=29 node=26 backend=OpenCL name=q_pe-15 op=ROPE
[split-node] split=29 node=27 backend=OpenCL name=q_nope-15 op=VIEW
[split-node] split=29 node=28 backend=OpenCL name=Qcur-15 op=CONCAT
[split-node] split=29 node=29 backend=OpenCL name=kv_cmpr_pe-15 op=MUL_MAT
[split-node] split=29 node=30 backend=OpenCL name=k_pe-15 op=VIEW
[split-node] split=29 node=31 backend=OpenCL name=k_pe-15 op=ROPE
[split-node] split=29 node=32 backend=OpenCL name=node_962 op=REPEAT
[split-node] split=29 node=33 backend=OpenCL name=kv_cmpr-15 op=VIEW
[split-node] split=29 node=34 backend=OpenCL name=norm-15 op=RMS_NORM
[split-node] split=29 node=35 backend=OpenCL name=kv_cmpr-15 op=MUL
[split-node] split=29 node=36 backend=OpenCL name=kv-15 op=MUL_MAT
[split-node] split=29 node=37 backend=OpenCL name=k_nope_view-15 op=VIEW
[split-node] split=29 node=38 backend=OpenCL name=Kcur-15 op=CONCAT
[split-node] split=29 node=39 backend=OpenCL name=Vcur_view-15 op=VIEW
[split-node] split=29 node=40 backend=OpenCL name=Vcur_cont-15 op=CONT
[split-node] split=29 node=41 backend=OpenCL name=Kcur-15 (view) op=VIEW
[split-node] split=29 node=42 backend=OpenCL name=cache_k_l15 (view) op=SET_ROWS
[split-node] split=29 node=43 backend=OpenCL name=Vcur_cont-15 (view) op=VIEW
[split-node] split=29 node=44 backend=OpenCL name=cache_v_l15 (view) op=SET_ROWS
[split-node] split=29 node=45 backend=OpenCL name=Qcur-15 (view) op=VIEW
[split-node] split=29 node=46 backend=OpenCL name=Qcur-15 (view) (permuted) op=PERMUTE
[split-node] split=29 node=47 backend=OpenCL name=cache_k_l15 (view) op=VIEW
[split-node] split=29 node=48 backend=OpenCL name=cache_k_l15 (view) (permuted) op=PERMUTE
[split-node] split=29 node=49 backend=OpenCL name=cache_v_l15 (view) op=VIEW
[split-node] split=29 node=50 backend=OpenCL name=cache_v_l15 (view) (permuted) op=PERMUTE
[split-node] split=29 node=51 backend=OpenCL name=__fattn__-15 op=FLASH_ATTN_BACK
[split-node] split=29 node=52 backend=OpenCL name=kqv_out-15 op=RESHAPE
[split-node] split=29 node=53 backend=OpenCL name=node_983 op=MUL_MAT
[split-node] split=29 node=54 backend=OpenCL name=ffn_inp-15 op=ADD
[split-node] split=29 node=55 backend=OpenCL name=norm-15 op=RMS_NORM
[split-node] split=29 node=56 backend=OpenCL name=ffn_norm-15 op=MUL
[split-node] split=29 node=57 backend=OpenCL name=ffn_moe_logits-15 op=MUL_MAT
[split-node] split=29 node=58 backend=OpenCL name=ffn_moe_probs-15 op=SOFT_MAX
[split-node] split=29 node=59 backend=OpenCL name=ffn_moe_probs-15 (reshaped) op=RESHAPE
[split-node] split=29 node=60 backend=OpenCL name=ffn_moe_argsort-15 op=ARGSORT
[split-node] split=29 node=61 backend=OpenCL name=ffn_moe_topk-15 op=VIEW
[split-node] split=29 node=62 backend=OpenCL name=ffn_moe_weights-15 op=GET_ROWS
[split-input] split=29 name=ffn_moe_weights_scaled-14 bytes=12288 backend_dst=OpenCL
[split-input] split=29 name=ffn_moe_topk-15 bytes=130840 backend_dst=OpenCL
[split-summary] id=30 backend=CPU nodes=2 inputs=1
[split-node] split=30 node=0 backend=CPU name=ffn_moe_weights_scaled-15 op=SCALE
[split-node] split=30 node=1 backend=OpenCL name=ffn_norm-15 (reshaped) op=RESHAPE
[split-input] split=30 name=ffn_moe_weights-15 bytes=12288 backend_dst=CPU
[split-summary] id=31 backend=OpenCL nodes=63 inputs=2
[split-node] split=31 node=0 backend=OpenCL name=ffn_moe_gate-15 op=MUL_MAT_ID
[split-node] split=31 node=1 backend=OpenCL name=ffn_moe_up-15 op=MUL_MAT_ID
[split-node] split=31 node=2 backend=OpenCL name=ffn_moe_weighted-15 op=(null)
[split-node] split=31 node=3 backend=OpenCL name=ffn_moe_down-15 op=MUL_MAT_ID
[split-node] split=31 node=4 backend=OpenCL name=node_999 op=MUL
[split-node] split=31 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=31 node=6 backend=OpenCL name=node_999 (view) op=VIEW
[split-node] split=31 node=7 backend=OpenCL name=node_999 (view) op=VIEW
[split-node] split=31 node=8 backend=OpenCL name=node_999 (view) op=VIEW
[split-node] split=31 node=9 backend=OpenCL name=node_999 (view) op=VIEW
[split-node] split=31 node=10 backend=OpenCL name=node_999 (view) op=VIEW
[split-node] split=31 node=11 backend=OpenCL name=ffn_gate-15 op=MUL_MAT
[split-node] split=31 node=12 backend=OpenCL name=ffn_up-15 op=MUL_MAT
[split-node] split=31 node=13 backend=OpenCL name=ffn_swiglu-15 op=(null)
[split-node] split=31 node=14 backend=OpenCL name=node_1009 op=ADD
[split-node] split=31 node=15 backend=OpenCL name=node_1010 op=ADD
[split-node] split=31 node=16 backend=OpenCL name=node_1011 op=ADD
[split-node] split=31 node=17 backend=OpenCL name=node_1012 op=ADD
[split-node] split=31 node=18 backend=OpenCL name=ffn_moe_out-15 op=ADD
[split-node] split=31 node=19 backend=OpenCL name=ffn_shexp-15 op=MUL_MAT
[split-node] split=31 node=20 backend=OpenCL name=ffn_out-15 op=ADD
[split-node] split=31 node=21 backend=OpenCL name=l_out-15 op=ADD
[split-node] split=31 node=22 backend=OpenCL name=norm-16 op=RMS_NORM
[split-node] split=31 node=23 backend=OpenCL name=attn_norm-16 op=MUL
[split-node] split=31 node=24 backend=OpenCL name=q-16 op=MUL_MAT
[split-node] split=31 node=25 backend=OpenCL name=q_pe-16 op=VIEW
[split-node] split=31 node=26 backend=OpenCL name=q_pe-16 op=ROPE
[split-node] split=31 node=27 backend=OpenCL name=q_nope-16 op=VIEW
[split-node] split=31 node=28 backend=OpenCL name=Qcur-16 op=CONCAT
[split-node] split=31 node=29 backend=OpenCL name=kv_cmpr_pe-16 op=MUL_MAT
[split-node] split=31 node=30 backend=OpenCL name=k_pe-16 op=VIEW
[split-node] split=31 node=31 backend=OpenCL name=k_pe-16 op=ROPE
[split-node] split=31 node=32 backend=OpenCL name=node_1027 op=REPEAT
[split-node] split=31 node=33 backend=OpenCL name=kv_cmpr-16 op=VIEW
[split-node] split=31 node=34 backend=OpenCL name=norm-16 op=RMS_NORM
[split-node] split=31 node=35 backend=OpenCL name=kv_cmpr-16 op=MUL
[split-node] split=31 node=36 backend=OpenCL name=kv-16 op=MUL_MAT
[split-node] split=31 node=37 backend=OpenCL name=k_nope_view-16 op=VIEW
[split-node] split=31 node=38 backend=OpenCL name=Kcur-16 op=CONCAT
[split-node] split=31 node=39 backend=OpenCL name=Vcur_view-16 op=VIEW
[split-node] split=31 node=40 backend=OpenCL name=Vcur_cont-16 op=CONT
[split-node] split=31 node=41 backend=OpenCL name=Kcur-16 (view) op=VIEW
[split-node] split=31 node=42 backend=OpenCL name=cache_k_l16 (view) op=SET_ROWS
[split-node] split=31 node=43 backend=OpenCL name=Vcur_cont-16 (view) op=VIEW
[split-node] split=31 node=44 backend=OpenCL name=cache_v_l16 (view) op=SET_ROWS
[split-node] split=31 node=45 backend=OpenCL name=Qcur-16 (view) op=VIEW
[split-node] split=31 node=46 backend=OpenCL name=Qcur-16 (view) (permuted) op=PERMUTE
[split-node] split=31 node=47 backend=OpenCL name=cache_k_l16 (view) op=VIEW
[split-node] split=31 node=48 backend=OpenCL name=cache_k_l16 (view) (permuted) op=PERMUTE
[split-node] split=31 node=49 backend=OpenCL name=cache_v_l16 (view) op=VIEW
[split-node] split=31 node=50 backend=OpenCL name=cache_v_l16 (view) (permuted) op=PERMUTE
[split-node] split=31 node=51 backend=OpenCL name=__fattn__-16 op=FLASH_ATTN_BACK
[split-node] split=31 node=52 backend=OpenCL name=kqv_out-16 op=RESHAPE
[split-node] split=31 node=53 backend=OpenCL name=node_1048 op=MUL_MAT
[split-node] split=31 node=54 backend=OpenCL name=ffn_inp-16 op=ADD
[split-node] split=31 node=55 backend=OpenCL name=norm-16 op=RMS_NORM
[split-node] split=31 node=56 backend=OpenCL name=ffn_norm-16 op=MUL
[split-node] split=31 node=57 backend=OpenCL name=ffn_moe_logits-16 op=MUL_MAT
[split-node] split=31 node=58 backend=OpenCL name=ffn_moe_probs-16 op=SOFT_MAX
[split-node] split=31 node=59 backend=OpenCL name=ffn_moe_probs-16 (reshaped) op=RESHAPE
[split-node] split=31 node=60 backend=OpenCL name=ffn_moe_argsort-16 op=ARGSORT
[split-node] split=31 node=61 backend=OpenCL name=ffn_moe_topk-16 op=VIEW
[split-node] split=31 node=62 backend=OpenCL name=ffn_moe_weights-16 op=GET_ROWS
[split-input] split=31 name=ffn_moe_weights_scaled-15 bytes=12288 backend_dst=OpenCL
[split-input] split=31 name=ffn_moe_topk-16 bytes=130840 backend_dst=OpenCL
[split-summary] id=32 backend=CPU nodes=2 inputs=1
[split-node] split=32 node=0 backend=CPU name=ffn_moe_weights_scaled-16 op=SCALE
[split-node] split=32 node=1 backend=OpenCL name=ffn_norm-16 (reshaped) op=RESHAPE
[split-input] split=32 name=ffn_moe_weights-16 bytes=12288 backend_dst=CPU
[split-summary] id=33 backend=OpenCL nodes=63 inputs=2
[split-node] split=33 node=0 backend=OpenCL name=ffn_moe_gate-16 op=MUL_MAT_ID
[split-node] split=33 node=1 backend=OpenCL name=ffn_moe_up-16 op=MUL_MAT_ID
[split-node] split=33 node=2 backend=OpenCL name=ffn_moe_weighted-16 op=(null)
[split-node] split=33 node=3 backend=OpenCL name=ffn_moe_down-16 op=MUL_MAT_ID
[split-node] split=33 node=4 backend=OpenCL name=node_1064 op=MUL
[split-node] split=33 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=33 node=6 backend=OpenCL name=node_1064 (view) op=VIEW
[split-node] split=33 node=7 backend=OpenCL name=node_1064 (view) op=VIEW
[split-node] split=33 node=8 backend=OpenCL name=node_1064 (view) op=VIEW
[split-node] split=33 node=9 backend=OpenCL name=node_1064 (view) op=VIEW
[split-node] split=33 node=10 backend=OpenCL name=node_1064 (view) op=VIEW
[split-node] split=33 node=11 backend=OpenCL name=ffn_gate-16 op=MUL_MAT
[split-node] split=33 node=12 backend=OpenCL name=ffn_up-16 op=MUL_MAT
[split-node] split=33 node=13 backend=OpenCL name=ffn_swiglu-16 op=(null)
[split-node] split=33 node=14 backend=OpenCL name=node_1074 op=ADD
[split-node] split=33 node=15 backend=OpenCL name=node_1075 op=ADD
[split-node] split=33 node=16 backend=OpenCL name=node_1076 op=ADD
[split-node] split=33 node=17 backend=OpenCL name=node_1077 op=ADD
[split-node] split=33 node=18 backend=OpenCL name=ffn_moe_out-16 op=ADD
[split-node] split=33 node=19 backend=OpenCL name=ffn_shexp-16 op=MUL_MAT
[split-node] split=33 node=20 backend=OpenCL name=ffn_out-16 op=ADD
[split-node] split=33 node=21 backend=OpenCL name=l_out-16 op=ADD
[split-node] split=33 node=22 backend=OpenCL name=norm-17 op=RMS_NORM
[split-node] split=33 node=23 backend=OpenCL name=attn_norm-17 op=MUL
[split-node] split=33 node=24 backend=OpenCL name=q-17 op=MUL_MAT
[split-node] split=33 node=25 backend=OpenCL name=q_pe-17 op=VIEW
[split-node] split=33 node=26 backend=OpenCL name=q_pe-17 op=ROPE
[split-node] split=33 node=27 backend=OpenCL name=q_nope-17 op=VIEW
[split-node] split=33 node=28 backend=OpenCL name=Qcur-17 op=CONCAT
[split-node] split=33 node=29 backend=OpenCL name=kv_cmpr_pe-17 op=MUL_MAT
[split-node] split=33 node=30 backend=OpenCL name=k_pe-17 op=VIEW
[split-node] split=33 node=31 backend=OpenCL name=k_pe-17 op=ROPE
[split-node] split=33 node=32 backend=OpenCL name=node_1092 op=REPEAT
[split-node] split=33 node=33 backend=OpenCL name=kv_cmpr-17 op=VIEW
[split-node] split=33 node=34 backend=OpenCL name=norm-17 op=RMS_NORM
[split-node] split=33 node=35 backend=OpenCL name=kv_cmpr-17 op=MUL
[split-node] split=33 node=36 backend=OpenCL name=kv-17 op=MUL_MAT
[split-node] split=33 node=37 backend=OpenCL name=k_nope_view-17 op=VIEW
[split-node] split=33 node=38 backend=OpenCL name=Kcur-17 op=CONCAT
[split-node] split=33 node=39 backend=OpenCL name=Vcur_view-17 op=VIEW
[split-node] split=33 node=40 backend=OpenCL name=Vcur_cont-17 op=CONT
[split-node] split=33 node=41 backend=OpenCL name=Kcur-17 (view) op=VIEW
[split-node] split=33 node=42 backend=OpenCL name=cache_k_l17 (view) op=SET_ROWS
[split-node] split=33 node=43 backend=OpenCL name=Vcur_cont-17 (view) op=VIEW
[split-node] split=33 node=44 backend=OpenCL name=cache_v_l17 (view) op=SET_ROWS
[split-node] split=33 node=45 backend=OpenCL name=Qcur-17 (view) op=VIEW
[split-node] split=33 node=46 backend=OpenCL name=Qcur-17 (view) (permuted) op=PERMUTE
[split-node] split=33 node=47 backend=OpenCL name=cache_k_l17 (view) op=VIEW
[split-node] split=33 node=48 backend=OpenCL name=cache_k_l17 (view) (permuted) op=PERMUTE
[split-node] split=33 node=49 backend=OpenCL name=cache_v_l17 (view) op=VIEW
[split-node] split=33 node=50 backend=OpenCL name=cache_v_l17 (view) (permuted) op=PERMUTE
[split-node] split=33 node=51 backend=OpenCL name=__fattn__-17 op=FLASH_ATTN_BACK
[split-node] split=33 node=52 backend=OpenCL name=kqv_out-17 op=RESHAPE
[split-node] split=33 node=53 backend=OpenCL name=node_1113 op=MUL_MAT
[split-node] split=33 node=54 backend=OpenCL name=ffn_inp-17 op=ADD
[split-node] split=33 node=55 backend=OpenCL name=norm-17 op=RMS_NORM
[split-node] split=33 node=56 backend=OpenCL name=ffn_norm-17 op=MUL
[split-node] split=33 node=57 backend=OpenCL name=ffn_moe_logits-17 op=MUL_MAT
[split-node] split=33 node=58 backend=OpenCL name=ffn_moe_probs-17 op=SOFT_MAX
[split-node] split=33 node=59 backend=OpenCL name=ffn_moe_probs-17 (reshaped) op=RESHAPE
[split-node] split=33 node=60 backend=OpenCL name=ffn_moe_argsort-17 op=ARGSORT
[split-node] split=33 node=61 backend=OpenCL name=ffn_moe_topk-17 op=VIEW
[split-node] split=33 node=62 backend=OpenCL name=ffn_moe_weights-17 op=GET_ROWS
[split-input] split=33 name=ffn_moe_weights_scaled-16 bytes=12288 backend_dst=OpenCL
[split-input] split=33 name=ffn_moe_topk-17 bytes=130840 backend_dst=OpenCL
[split-summary] id=34 backend=CPU nodes=2 inputs=1
[split-node] split=34 node=0 backend=CPU name=ffn_moe_weights_scaled-17 op=SCALE
[split-node] split=34 node=1 backend=OpenCL name=ffn_norm-17 (reshaped) op=RESHAPE
[split-input] split=34 name=ffn_moe_weights-17 bytes=12288 backend_dst=CPU
[split-summary] id=35 backend=OpenCL nodes=63 inputs=2
[split-node] split=35 node=0 backend=OpenCL name=ffn_moe_gate-17 op=MUL_MAT_ID
[split-node] split=35 node=1 backend=OpenCL name=ffn_moe_up-17 op=MUL_MAT_ID
[split-node] split=35 node=2 backend=OpenCL name=ffn_moe_weighted-17 op=(null)
[split-node] split=35 node=3 backend=OpenCL name=ffn_moe_down-17 op=MUL_MAT_ID
[split-node] split=35 node=4 backend=OpenCL name=node_1129 op=MUL
[split-node] split=35 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=35 node=6 backend=OpenCL name=node_1129 (view) op=VIEW
[split-node] split=35 node=7 backend=OpenCL name=node_1129 (view) op=VIEW
[split-node] split=35 node=8 backend=OpenCL name=node_1129 (view) op=VIEW
[split-node] split=35 node=9 backend=OpenCL name=node_1129 (view) op=VIEW
[split-node] split=35 node=10 backend=OpenCL name=node_1129 (view) op=VIEW
[split-node] split=35 node=11 backend=OpenCL name=ffn_gate-17 op=MUL_MAT
[split-node] split=35 node=12 backend=OpenCL name=ffn_up-17 op=MUL_MAT
[split-node] split=35 node=13 backend=OpenCL name=ffn_swiglu-17 op=(null)
[split-node] split=35 node=14 backend=OpenCL name=node_1139 op=ADD
[split-node] split=35 node=15 backend=OpenCL name=node_1140 op=ADD
[split-node] split=35 node=16 backend=OpenCL name=node_1141 op=ADD
[split-node] split=35 node=17 backend=OpenCL name=node_1142 op=ADD
[split-node] split=35 node=18 backend=OpenCL name=ffn_moe_out-17 op=ADD
[split-node] split=35 node=19 backend=OpenCL name=ffn_shexp-17 op=MUL_MAT
[split-node] split=35 node=20 backend=OpenCL name=ffn_out-17 op=ADD
[split-node] split=35 node=21 backend=OpenCL name=l_out-17 op=ADD
[split-node] split=35 node=22 backend=OpenCL name=norm-18 op=RMS_NORM
[split-node] split=35 node=23 backend=OpenCL name=attn_norm-18 op=MUL
[split-node] split=35 node=24 backend=OpenCL name=q-18 op=MUL_MAT
[split-node] split=35 node=25 backend=OpenCL name=q_pe-18 op=VIEW
[split-node] split=35 node=26 backend=OpenCL name=q_pe-18 op=ROPE
[split-node] split=35 node=27 backend=OpenCL name=q_nope-18 op=VIEW
[split-node] split=35 node=28 backend=OpenCL name=Qcur-18 op=CONCAT
[split-node] split=35 node=29 backend=OpenCL name=kv_cmpr_pe-18 op=MUL_MAT
[split-node] split=35 node=30 backend=OpenCL name=k_pe-18 op=VIEW
[split-node] split=35 node=31 backend=OpenCL name=k_pe-18 op=ROPE
[split-node] split=35 node=32 backend=OpenCL name=node_1157 op=REPEAT
[split-node] split=35 node=33 backend=OpenCL name=kv_cmpr-18 op=VIEW
[split-node] split=35 node=34 backend=OpenCL name=norm-18 op=RMS_NORM
[split-node] split=35 node=35 backend=OpenCL name=kv_cmpr-18 op=MUL
[split-node] split=35 node=36 backend=OpenCL name=kv-18 op=MUL_MAT
[split-node] split=35 node=37 backend=OpenCL name=k_nope_view-18 op=VIEW
[split-node] split=35 node=38 backend=OpenCL name=Kcur-18 op=CONCAT
[split-node] split=35 node=39 backend=OpenCL name=Vcur_view-18 op=VIEW
[split-node] split=35 node=40 backend=OpenCL name=Vcur_cont-18 op=CONT
[split-node] split=35 node=41 backend=OpenCL name=Kcur-18 (view) op=VIEW
[split-node] split=35 node=42 backend=OpenCL name=cache_k_l18 (view) op=SET_ROWS
[split-node] split=35 node=43 backend=OpenCL name=Vcur_cont-18 (view) op=VIEW
[split-node] split=35 node=44 backend=OpenCL name=cache_v_l18 (view) op=SET_ROWS
[split-node] split=35 node=45 backend=OpenCL name=Qcur-18 (view) op=VIEW
[split-node] split=35 node=46 backend=OpenCL name=Qcur-18 (view) (permuted) op=PERMUTE
[split-node] split=35 node=47 backend=OpenCL name=cache_k_l18 (view) op=VIEW
[split-node] split=35 node=48 backend=OpenCL name=cache_k_l18 (view) (permuted) op=PERMUTE
[split-node] split=35 node=49 backend=OpenCL name=cache_v_l18 (view) op=VIEW
[split-node] split=35 node=50 backend=OpenCL name=cache_v_l18 (view) (permuted) op=PERMUTE
[split-node] split=35 node=51 backend=OpenCL name=__fattn__-18 op=FLASH_ATTN_BACK
[split-node] split=35 node=52 backend=OpenCL name=kqv_out-18 op=RESHAPE
[split-node] split=35 node=53 backend=OpenCL name=node_1178 op=MUL_MAT
[split-node] split=35 node=54 backend=OpenCL name=ffn_inp-18 op=ADD
[split-node] split=35 node=55 backend=OpenCL name=norm-18 op=RMS_NORM
[split-node] split=35 node=56 backend=OpenCL name=ffn_norm-18 op=MUL
[split-node] split=35 node=57 backend=OpenCL name=ffn_moe_logits-18 op=MUL_MAT
[split-node] split=35 node=58 backend=OpenCL name=ffn_moe_probs-18 op=SOFT_MAX
[split-node] split=35 node=59 backend=OpenCL name=ffn_moe_probs-18 (reshaped) op=RESHAPE
[split-node] split=35 node=60 backend=OpenCL name=ffn_moe_argsort-18 op=ARGSORT
[split-node] split=35 node=61 backend=OpenCL name=ffn_moe_topk-18 op=VIEW
[split-node] split=35 node=62 backend=OpenCL name=ffn_moe_weights-18 op=GET_ROWS
[split-input] split=35 name=ffn_moe_weights_scaled-17 bytes=12288 backend_dst=OpenCL
[split-input] split=35 name=ffn_moe_topk-18 bytes=130840 backend_dst=OpenCL
[split-summary] id=36 backend=CPU nodes=2 inputs=1
[split-node] split=36 node=0 backend=CPU name=ffn_moe_weights_scaled-18 op=SCALE
[split-node] split=36 node=1 backend=OpenCL name=ffn_norm-18 (reshaped) op=RESHAPE
[split-input] split=36 name=ffn_moe_weights-18 bytes=12288 backend_dst=CPU
[split-summary] id=37 backend=OpenCL nodes=63 inputs=2
[split-node] split=37 node=0 backend=OpenCL name=ffn_moe_gate-18 op=MUL_MAT_ID
[split-node] split=37 node=1 backend=OpenCL name=ffn_moe_up-18 op=MUL_MAT_ID
[split-node] split=37 node=2 backend=OpenCL name=ffn_moe_weighted-18 op=(null)
[split-node] split=37 node=3 backend=OpenCL name=ffn_moe_down-18 op=MUL_MAT_ID
[split-node] split=37 node=4 backend=OpenCL name=node_1194 op=MUL
[split-node] split=37 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=37 node=6 backend=OpenCL name=node_1194 (view) op=VIEW
[split-node] split=37 node=7 backend=OpenCL name=node_1194 (view) op=VIEW
[split-node] split=37 node=8 backend=OpenCL name=node_1194 (view) op=VIEW
[split-node] split=37 node=9 backend=OpenCL name=node_1194 (view) op=VIEW
[split-node] split=37 node=10 backend=OpenCL name=node_1194 (view) op=VIEW
[split-node] split=37 node=11 backend=OpenCL name=ffn_gate-18 op=MUL_MAT
[split-node] split=37 node=12 backend=OpenCL name=ffn_up-18 op=MUL_MAT
[split-node] split=37 node=13 backend=OpenCL name=ffn_swiglu-18 op=(null)
[split-node] split=37 node=14 backend=OpenCL name=node_1204 op=ADD
[split-node] split=37 node=15 backend=OpenCL name=node_1205 op=ADD
[split-node] split=37 node=16 backend=OpenCL name=node_1206 op=ADD
[split-node] split=37 node=17 backend=OpenCL name=node_1207 op=ADD
[split-node] split=37 node=18 backend=OpenCL name=ffn_moe_out-18 op=ADD
[split-node] split=37 node=19 backend=OpenCL name=ffn_shexp-18 op=MUL_MAT
[split-node] split=37 node=20 backend=OpenCL name=ffn_out-18 op=ADD
[split-node] split=37 node=21 backend=OpenCL name=l_out-18 op=ADD
[split-node] split=37 node=22 backend=OpenCL name=norm-19 op=RMS_NORM
[split-node] split=37 node=23 backend=OpenCL name=attn_norm-19 op=MUL
[split-node] split=37 node=24 backend=OpenCL name=q-19 op=MUL_MAT
[split-node] split=37 node=25 backend=OpenCL name=q_pe-19 op=VIEW
[split-node] split=37 node=26 backend=OpenCL name=q_pe-19 op=ROPE
[split-node] split=37 node=27 backend=OpenCL name=q_nope-19 op=VIEW
[split-node] split=37 node=28 backend=OpenCL name=Qcur-19 op=CONCAT
[split-node] split=37 node=29 backend=OpenCL name=kv_cmpr_pe-19 op=MUL_MAT
[split-node] split=37 node=30 backend=OpenCL name=k_pe-19 op=VIEW
[split-node] split=37 node=31 backend=OpenCL name=k_pe-19 op=ROPE
[split-node] split=37 node=32 backend=OpenCL name=node_1222 op=REPEAT
[split-node] split=37 node=33 backend=OpenCL name=kv_cmpr-19 op=VIEW
[split-node] split=37 node=34 backend=OpenCL name=norm-19 op=RMS_NORM
[split-node] split=37 node=35 backend=OpenCL name=kv_cmpr-19 op=MUL
[split-node] split=37 node=36 backend=OpenCL name=kv-19 op=MUL_MAT
[split-node] split=37 node=37 backend=OpenCL name=k_nope_view-19 op=VIEW
[split-node] split=37 node=38 backend=OpenCL name=Kcur-19 op=CONCAT
[split-node] split=37 node=39 backend=OpenCL name=Vcur_view-19 op=VIEW
[split-node] split=37 node=40 backend=OpenCL name=Vcur_cont-19 op=CONT
[split-node] split=37 node=41 backend=OpenCL name=Kcur-19 (view) op=VIEW
[split-node] split=37 node=42 backend=OpenCL name=cache_k_l19 (view) op=SET_ROWS
[split-node] split=37 node=43 backend=OpenCL name=Vcur_cont-19 (view) op=VIEW
[split-node] split=37 node=44 backend=OpenCL name=cache_v_l19 (view) op=SET_ROWS
[split-node] split=37 node=45 backend=OpenCL name=Qcur-19 (view) op=VIEW
[split-node] split=37 node=46 backend=OpenCL name=Qcur-19 (view) (permuted) op=PERMUTE
[split-node] split=37 node=47 backend=OpenCL name=cache_k_l19 (view) op=VIEW
[split-node] split=37 node=48 backend=OpenCL name=cache_k_l19 (view) (permuted) op=PERMUTE
[split-node] split=37 node=49 backend=OpenCL name=cache_v_l19 (view) op=VIEW
[split-node] split=37 node=50 backend=OpenCL name=cache_v_l19 (view) (permuted) op=PERMUTE
[split-node] split=37 node=51 backend=OpenCL name=__fattn__-19 op=FLASH_ATTN_BACK
[split-node] split=37 node=52 backend=OpenCL name=kqv_out-19 op=RESHAPE
[split-node] split=37 node=53 backend=OpenCL name=node_1243 op=MUL_MAT
[split-node] split=37 node=54 backend=OpenCL name=ffn_inp-19 op=ADD
[split-node] split=37 node=55 backend=OpenCL name=norm-19 op=RMS_NORM
[split-node] split=37 node=56 backend=OpenCL name=ffn_norm-19 op=MUL
[split-node] split=37 node=57 backend=OpenCL name=ffn_moe_logits-19 op=MUL_MAT
[split-node] split=37 node=58 backend=OpenCL name=ffn_moe_probs-19 op=SOFT_MAX
[split-node] split=37 node=59 backend=OpenCL name=ffn_moe_probs-19 (reshaped) op=RESHAPE
[split-node] split=37 node=60 backend=OpenCL name=ffn_moe_argsort-19 op=ARGSORT
[split-node] split=37 node=61 backend=OpenCL name=ffn_moe_topk-19 op=VIEW
[split-node] split=37 node=62 backend=OpenCL name=ffn_moe_weights-19 op=GET_ROWS
[split-input] split=37 name=ffn_moe_weights_scaled-18 bytes=12288 backend_dst=OpenCL
[split-input] split=37 name=ffn_moe_topk-19 bytes=130840 backend_dst=OpenCL
[split-summary] id=38 backend=CPU nodes=2 inputs=1
[split-node] split=38 node=0 backend=CPU name=ffn_moe_weights_scaled-19 op=SCALE
[split-node] split=38 node=1 backend=OpenCL name=ffn_norm-19 (reshaped) op=RESHAPE
[split-input] split=38 name=ffn_moe_weights-19 bytes=12288 backend_dst=CPU
[split-summary] id=39 backend=OpenCL nodes=63 inputs=2
[split-node] split=39 node=0 backend=OpenCL name=ffn_moe_gate-19 op=MUL_MAT_ID
[split-node] split=39 node=1 backend=OpenCL name=ffn_moe_up-19 op=MUL_MAT_ID
[split-node] split=39 node=2 backend=OpenCL name=ffn_moe_weighted-19 op=(null)
[split-node] split=39 node=3 backend=OpenCL name=ffn_moe_down-19 op=MUL_MAT_ID
[split-node] split=39 node=4 backend=OpenCL name=node_1259 op=MUL
[split-node] split=39 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=39 node=6 backend=OpenCL name=node_1259 (view) op=VIEW
[split-node] split=39 node=7 backend=OpenCL name=node_1259 (view) op=VIEW
[split-node] split=39 node=8 backend=OpenCL name=node_1259 (view) op=VIEW
[split-node] split=39 node=9 backend=OpenCL name=node_1259 (view) op=VIEW
[split-node] split=39 node=10 backend=OpenCL name=node_1259 (view) op=VIEW
[split-node] split=39 node=11 backend=OpenCL name=ffn_gate-19 op=MUL_MAT
[split-node] split=39 node=12 backend=OpenCL name=ffn_up-19 op=MUL_MAT
[split-node] split=39 node=13 backend=OpenCL name=ffn_swiglu-19 op=(null)
[split-node] split=39 node=14 backend=OpenCL name=node_1269 op=ADD
[split-node] split=39 node=15 backend=OpenCL name=node_1270 op=ADD
[split-node] split=39 node=16 backend=OpenCL name=node_1271 op=ADD
[split-node] split=39 node=17 backend=OpenCL name=node_1272 op=ADD
[split-node] split=39 node=18 backend=OpenCL name=ffn_moe_out-19 op=ADD
[split-node] split=39 node=19 backend=OpenCL name=ffn_shexp-19 op=MUL_MAT
[split-node] split=39 node=20 backend=OpenCL name=ffn_out-19 op=ADD
[split-node] split=39 node=21 backend=OpenCL name=l_out-19 op=ADD
[split-node] split=39 node=22 backend=OpenCL name=norm-20 op=RMS_NORM
[split-node] split=39 node=23 backend=OpenCL name=attn_norm-20 op=MUL
[split-node] split=39 node=24 backend=OpenCL name=q-20 op=MUL_MAT
[split-node] split=39 node=25 backend=OpenCL name=q_pe-20 op=VIEW
[split-node] split=39 node=26 backend=OpenCL name=q_pe-20 op=ROPE
[split-node] split=39 node=27 backend=OpenCL name=q_nope-20 op=VIEW
[split-node] split=39 node=28 backend=OpenCL name=Qcur-20 op=CONCAT
[split-node] split=39 node=29 backend=OpenCL name=kv_cmpr_pe-20 op=MUL_MAT
[split-node] split=39 node=30 backend=OpenCL name=k_pe-20 op=VIEW
[split-node] split=39 node=31 backend=OpenCL name=k_pe-20 op=ROPE
[split-node] split=39 node=32 backend=OpenCL name=node_1287 op=REPEAT
[split-node] split=39 node=33 backend=OpenCL name=kv_cmpr-20 op=VIEW
[split-node] split=39 node=34 backend=OpenCL name=norm-20 op=RMS_NORM
[split-node] split=39 node=35 backend=OpenCL name=kv_cmpr-20 op=MUL
[split-node] split=39 node=36 backend=OpenCL name=kv-20 op=MUL_MAT
[split-node] split=39 node=37 backend=OpenCL name=k_nope_view-20 op=VIEW
[split-node] split=39 node=38 backend=OpenCL name=Kcur-20 op=CONCAT
[split-node] split=39 node=39 backend=OpenCL name=Vcur_view-20 op=VIEW
[split-node] split=39 node=40 backend=OpenCL name=Vcur_cont-20 op=CONT
[split-node] split=39 node=41 backend=OpenCL name=Kcur-20 (view) op=VIEW
[split-node] split=39 node=42 backend=OpenCL name=cache_k_l20 (view) op=SET_ROWS
[split-node] split=39 node=43 backend=OpenCL name=Vcur_cont-20 (view) op=VIEW
[split-node] split=39 node=44 backend=OpenCL name=cache_v_l20 (view) op=SET_ROWS
[split-node] split=39 node=45 backend=OpenCL name=Qcur-20 (view) op=VIEW
[split-node] split=39 node=46 backend=OpenCL name=Qcur-20 (view) (permuted) op=PERMUTE
[split-node] split=39 node=47 backend=OpenCL name=cache_k_l20 (view) op=VIEW
[split-node] split=39 node=48 backend=OpenCL name=cache_k_l20 (view) (permuted) op=PERMUTE
[split-node] split=39 node=49 backend=OpenCL name=cache_v_l20 (view) op=VIEW
[split-node] split=39 node=50 backend=OpenCL name=cache_v_l20 (view) (permuted) op=PERMUTE
[split-node] split=39 node=51 backend=OpenCL name=__fattn__-20 op=FLASH_ATTN_BACK
[split-node] split=39 node=52 backend=OpenCL name=kqv_out-20 op=RESHAPE
[split-node] split=39 node=53 backend=OpenCL name=node_1308 op=MUL_MAT
[split-node] split=39 node=54 backend=OpenCL name=ffn_inp-20 op=ADD
[split-node] split=39 node=55 backend=OpenCL name=norm-20 op=RMS_NORM
[split-node] split=39 node=56 backend=OpenCL name=ffn_norm-20 op=MUL
[split-node] split=39 node=57 backend=OpenCL name=ffn_moe_logits-20 op=MUL_MAT
[split-node] split=39 node=58 backend=OpenCL name=ffn_moe_probs-20 op=SOFT_MAX
[split-node] split=39 node=59 backend=OpenCL name=ffn_moe_probs-20 (reshaped) op=RESHAPE
[split-node] split=39 node=60 backend=OpenCL name=ffn_moe_argsort-20 op=ARGSORT
[split-node] split=39 node=61 backend=OpenCL name=ffn_moe_topk-20 op=VIEW
[split-node] split=39 node=62 backend=OpenCL name=ffn_moe_weights-20 op=GET_ROWS
[split-input] split=39 name=ffn_moe_weights_scaled-19 bytes=12288 backend_dst=OpenCL
[split-input] split=39 name=ffn_moe_topk-20 bytes=130840 backend_dst=OpenCL
[split-summary] id=40 backend=CPU nodes=2 inputs=1
[split-node] split=40 node=0 backend=CPU name=ffn_moe_weights_scaled-20 op=SCALE
[split-node] split=40 node=1 backend=OpenCL name=ffn_norm-20 (reshaped) op=RESHAPE
[split-input] split=40 name=ffn_moe_weights-20 bytes=12288 backend_dst=CPU
[split-summary] id=41 backend=OpenCL nodes=63 inputs=2
[split-node] split=41 node=0 backend=OpenCL name=ffn_moe_gate-20 op=MUL_MAT_ID
[split-node] split=41 node=1 backend=OpenCL name=ffn_moe_up-20 op=MUL_MAT_ID
[split-node] split=41 node=2 backend=OpenCL name=ffn_moe_weighted-20 op=(null)
[split-node] split=41 node=3 backend=OpenCL name=ffn_moe_down-20 op=MUL_MAT_ID
[split-node] split=41 node=4 backend=OpenCL name=node_1324 op=MUL
[split-node] split=41 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=41 node=6 backend=OpenCL name=node_1324 (view) op=VIEW
[split-node] split=41 node=7 backend=OpenCL name=node_1324 (view) op=VIEW
[split-node] split=41 node=8 backend=OpenCL name=node_1324 (view) op=VIEW
[split-node] split=41 node=9 backend=OpenCL name=node_1324 (view) op=VIEW
[split-node] split=41 node=10 backend=OpenCL name=node_1324 (view) op=VIEW
[split-node] split=41 node=11 backend=OpenCL name=ffn_gate-20 op=MUL_MAT
[split-node] split=41 node=12 backend=OpenCL name=ffn_up-20 op=MUL_MAT
[split-node] split=41 node=13 backend=OpenCL name=ffn_swiglu-20 op=(null)
[split-node] split=41 node=14 backend=OpenCL name=node_1334 op=ADD
[split-node] split=41 node=15 backend=OpenCL name=node_1335 op=ADD
[split-node] split=41 node=16 backend=OpenCL name=node_1336 op=ADD
[split-node] split=41 node=17 backend=OpenCL name=node_1337 op=ADD
[split-node] split=41 node=18 backend=OpenCL name=ffn_moe_out-20 op=ADD
[split-node] split=41 node=19 backend=OpenCL name=ffn_shexp-20 op=MUL_MAT
[split-node] split=41 node=20 backend=OpenCL name=ffn_out-20 op=ADD
[split-node] split=41 node=21 backend=OpenCL name=l_out-20 op=ADD
[split-node] split=41 node=22 backend=OpenCL name=norm-21 op=RMS_NORM
[split-node] split=41 node=23 backend=OpenCL name=attn_norm-21 op=MUL
[split-node] split=41 node=24 backend=OpenCL name=q-21 op=MUL_MAT
[split-node] split=41 node=25 backend=OpenCL name=q_pe-21 op=VIEW
[split-node] split=41 node=26 backend=OpenCL name=q_pe-21 op=ROPE
[split-node] split=41 node=27 backend=OpenCL name=q_nope-21 op=VIEW
[split-node] split=41 node=28 backend=OpenCL name=Qcur-21 op=CONCAT
[split-node] split=41 node=29 backend=OpenCL name=kv_cmpr_pe-21 op=MUL_MAT
[split-node] split=41 node=30 backend=OpenCL name=k_pe-21 op=VIEW
[split-node] split=41 node=31 backend=OpenCL name=k_pe-21 op=ROPE
[split-node] split=41 node=32 backend=OpenCL name=node_1352 op=REPEAT
[split-node] split=41 node=33 backend=OpenCL name=kv_cmpr-21 op=VIEW
[split-node] split=41 node=34 backend=OpenCL name=norm-21 op=RMS_NORM
[split-node] split=41 node=35 backend=OpenCL name=kv_cmpr-21 op=MUL
[split-node] split=41 node=36 backend=OpenCL name=kv-21 op=MUL_MAT
[split-node] split=41 node=37 backend=OpenCL name=k_nope_view-21 op=VIEW
[split-node] split=41 node=38 backend=OpenCL name=Kcur-21 op=CONCAT
[split-node] split=41 node=39 backend=OpenCL name=Vcur_view-21 op=VIEW
[split-node] split=41 node=40 backend=OpenCL name=Vcur_cont-21 op=CONT
[split-node] split=41 node=41 backend=OpenCL name=Kcur-21 (view) op=VIEW
[split-node] split=41 node=42 backend=OpenCL name=cache_k_l21 (view) op=SET_ROWS
[split-node] split=41 node=43 backend=OpenCL name=Vcur_cont-21 (view) op=VIEW
[split-node] split=41 node=44 backend=OpenCL name=cache_v_l21 (view) op=SET_ROWS
[split-node] split=41 node=45 backend=OpenCL name=Qcur-21 (view) op=VIEW
[split-node] split=41 node=46 backend=OpenCL name=Qcur-21 (view) (permuted) op=PERMUTE
[split-node] split=41 node=47 backend=OpenCL name=cache_k_l21 (view) op=VIEW
[split-node] split=41 node=48 backend=OpenCL name=cache_k_l21 (view) (permuted) op=PERMUTE
[split-node] split=41 node=49 backend=OpenCL name=cache_v_l21 (view) op=VIEW
[split-node] split=41 node=50 backend=OpenCL name=cache_v_l21 (view) (permuted) op=PERMUTE
[split-node] split=41 node=51 backend=OpenCL name=__fattn__-21 op=FLASH_ATTN_BACK
[split-node] split=41 node=52 backend=OpenCL name=kqv_out-21 op=RESHAPE
[split-node] split=41 node=53 backend=OpenCL name=node_1373 op=MUL_MAT
[split-node] split=41 node=54 backend=OpenCL name=ffn_inp-21 op=ADD
[split-node] split=41 node=55 backend=OpenCL name=norm-21 op=RMS_NORM
[split-node] split=41 node=56 backend=OpenCL name=ffn_norm-21 op=MUL
[split-node] split=41 node=57 backend=OpenCL name=ffn_moe_logits-21 op=MUL_MAT
[split-node] split=41 node=58 backend=OpenCL name=ffn_moe_probs-21 op=SOFT_MAX
[split-node] split=41 node=59 backend=OpenCL name=ffn_moe_probs-21 (reshaped) op=RESHAPE
[split-node] split=41 node=60 backend=OpenCL name=ffn_moe_argsort-21 op=ARGSORT
[split-node] split=41 node=61 backend=OpenCL name=ffn_moe_topk-21 op=VIEW
[split-node] split=41 node=62 backend=OpenCL name=ffn_moe_weights-21 op=GET_ROWS
[split-input] split=41 name=ffn_moe_weights_scaled-20 bytes=12288 backend_dst=OpenCL
[split-input] split=41 name=ffn_moe_topk-21 bytes=130840 backend_dst=OpenCL
[split-summary] id=42 backend=CPU nodes=2 inputs=1
[split-node] split=42 node=0 backend=CPU name=ffn_moe_weights_scaled-21 op=SCALE
[split-node] split=42 node=1 backend=OpenCL name=ffn_norm-21 (reshaped) op=RESHAPE
[split-input] split=42 name=ffn_moe_weights-21 bytes=12288 backend_dst=CPU
[split-summary] id=43 backend=OpenCL nodes=63 inputs=2
[split-node] split=43 node=0 backend=OpenCL name=ffn_moe_gate-21 op=MUL_MAT_ID
[split-node] split=43 node=1 backend=OpenCL name=ffn_moe_up-21 op=MUL_MAT_ID
[split-node] split=43 node=2 backend=OpenCL name=ffn_moe_weighted-21 op=(null)
[split-node] split=43 node=3 backend=OpenCL name=ffn_moe_down-21 op=MUL_MAT_ID
[split-node] split=43 node=4 backend=OpenCL name=node_1389 op=MUL
[split-node] split=43 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=43 node=6 backend=OpenCL name=node_1389 (view) op=VIEW
[split-node] split=43 node=7 backend=OpenCL name=node_1389 (view) op=VIEW
[split-node] split=43 node=8 backend=OpenCL name=node_1389 (view) op=VIEW
[split-node] split=43 node=9 backend=OpenCL name=node_1389 (view) op=VIEW
[split-node] split=43 node=10 backend=OpenCL name=node_1389 (view) op=VIEW
[split-node] split=43 node=11 backend=OpenCL name=ffn_gate-21 op=MUL_MAT
[split-node] split=43 node=12 backend=OpenCL name=ffn_up-21 op=MUL_MAT
[split-node] split=43 node=13 backend=OpenCL name=ffn_swiglu-21 op=(null)
[split-node] split=43 node=14 backend=OpenCL name=node_1399 op=ADD
[split-node] split=43 node=15 backend=OpenCL name=node_1400 op=ADD
[split-node] split=43 node=16 backend=OpenCL name=node_1401 op=ADD
[split-node] split=43 node=17 backend=OpenCL name=node_1402 op=ADD
[split-node] split=43 node=18 backend=OpenCL name=ffn_moe_out-21 op=ADD
[split-node] split=43 node=19 backend=OpenCL name=ffn_shexp-21 op=MUL_MAT
[split-node] split=43 node=20 backend=OpenCL name=ffn_out-21 op=ADD
[split-node] split=43 node=21 backend=OpenCL name=l_out-21 op=ADD
[split-node] split=43 node=22 backend=OpenCL name=norm-22 op=RMS_NORM
[split-node] split=43 node=23 backend=OpenCL name=attn_norm-22 op=MUL
[split-node] split=43 node=24 backend=OpenCL name=q-22 op=MUL_MAT
[split-node] split=43 node=25 backend=OpenCL name=q_pe-22 op=VIEW
[split-node] split=43 node=26 backend=OpenCL name=q_pe-22 op=ROPE
[split-node] split=43 node=27 backend=OpenCL name=q_nope-22 op=VIEW
[split-node] split=43 node=28 backend=OpenCL name=Qcur-22 op=CONCAT
[split-node] split=43 node=29 backend=OpenCL name=kv_cmpr_pe-22 op=MUL_MAT
[split-node] split=43 node=30 backend=OpenCL name=k_pe-22 op=VIEW
[split-node] split=43 node=31 backend=OpenCL name=k_pe-22 op=ROPE
[split-node] split=43 node=32 backend=OpenCL name=node_1417 op=REPEAT
[split-node] split=43 node=33 backend=OpenCL name=kv_cmpr-22 op=VIEW
[split-node] split=43 node=34 backend=OpenCL name=norm-22 op=RMS_NORM
[split-node] split=43 node=35 backend=OpenCL name=kv_cmpr-22 op=MUL
[split-node] split=43 node=36 backend=OpenCL name=kv-22 op=MUL_MAT
[split-node] split=43 node=37 backend=OpenCL name=k_nope_view-22 op=VIEW
[split-node] split=43 node=38 backend=OpenCL name=Kcur-22 op=CONCAT
[split-node] split=43 node=39 backend=OpenCL name=Vcur_view-22 op=VIEW
[split-node] split=43 node=40 backend=OpenCL name=Vcur_cont-22 op=CONT
[split-node] split=43 node=41 backend=OpenCL name=Kcur-22 (view) op=VIEW
[split-node] split=43 node=42 backend=OpenCL name=cache_k_l22 (view) op=SET_ROWS
[split-node] split=43 node=43 backend=OpenCL name=Vcur_cont-22 (view) op=VIEW
[split-node] split=43 node=44 backend=OpenCL name=cache_v_l22 (view) op=SET_ROWS
[split-node] split=43 node=45 backend=OpenCL name=Qcur-22 (view) op=VIEW
[split-node] split=43 node=46 backend=OpenCL name=Qcur-22 (view) (permuted) op=PERMUTE
[split-node] split=43 node=47 backend=OpenCL name=cache_k_l22 (view) op=VIEW
[split-node] split=43 node=48 backend=OpenCL name=cache_k_l22 (view) (permuted) op=PERMUTE
[split-node] split=43 node=49 backend=OpenCL name=cache_v_l22 (view) op=VIEW
[split-node] split=43 node=50 backend=OpenCL name=cache_v_l22 (view) (permuted) op=PERMUTE
[split-node] split=43 node=51 backend=OpenCL name=__fattn__-22 op=FLASH_ATTN_BACK
[split-node] split=43 node=52 backend=OpenCL name=kqv_out-22 op=RESHAPE
[split-node] split=43 node=53 backend=OpenCL name=node_1438 op=MUL_MAT
[split-node] split=43 node=54 backend=OpenCL name=ffn_inp-22 op=ADD
[split-node] split=43 node=55 backend=OpenCL name=norm-22 op=RMS_NORM
[split-node] split=43 node=56 backend=OpenCL name=ffn_norm-22 op=MUL
[split-node] split=43 node=57 backend=OpenCL name=ffn_moe_logits-22 op=MUL_MAT
[split-node] split=43 node=58 backend=OpenCL name=ffn_moe_probs-22 op=SOFT_MAX
[split-node] split=43 node=59 backend=OpenCL name=ffn_moe_probs-22 (reshaped) op=RESHAPE
[split-node] split=43 node=60 backend=OpenCL name=ffn_moe_argsort-22 op=ARGSORT
[split-node] split=43 node=61 backend=OpenCL name=ffn_moe_topk-22 op=VIEW
[split-node] split=43 node=62 backend=OpenCL name=ffn_moe_weights-22 op=GET_ROWS
[split-input] split=43 name=ffn_moe_weights_scaled-21 bytes=12288 backend_dst=OpenCL
[split-input] split=43 name=ffn_moe_topk-22 bytes=130840 backend_dst=OpenCL
[split-summary] id=44 backend=CPU nodes=2 inputs=1
[split-node] split=44 node=0 backend=CPU name=ffn_moe_weights_scaled-22 op=SCALE
[split-node] split=44 node=1 backend=OpenCL name=ffn_norm-22 (reshaped) op=RESHAPE
[split-input] split=44 name=ffn_moe_weights-22 bytes=12288 backend_dst=CPU
[split-summary] id=45 backend=OpenCL nodes=63 inputs=2
[split-node] split=45 node=0 backend=OpenCL name=ffn_moe_gate-22 op=MUL_MAT_ID
[split-node] split=45 node=1 backend=OpenCL name=ffn_moe_up-22 op=MUL_MAT_ID
[split-node] split=45 node=2 backend=OpenCL name=ffn_moe_weighted-22 op=(null)
[split-node] split=45 node=3 backend=OpenCL name=ffn_moe_down-22 op=MUL_MAT_ID
[split-node] split=45 node=4 backend=OpenCL name=node_1454 op=MUL
[split-node] split=45 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=45 node=6 backend=OpenCL name=node_1454 (view) op=VIEW
[split-node] split=45 node=7 backend=OpenCL name=node_1454 (view) op=VIEW
[split-node] split=45 node=8 backend=OpenCL name=node_1454 (view) op=VIEW
[split-node] split=45 node=9 backend=OpenCL name=node_1454 (view) op=VIEW
[split-node] split=45 node=10 backend=OpenCL name=node_1454 (view) op=VIEW
[split-node] split=45 node=11 backend=OpenCL name=ffn_gate-22 op=MUL_MAT
[split-node] split=45 node=12 backend=OpenCL name=ffn_up-22 op=MUL_MAT
[split-node] split=45 node=13 backend=OpenCL name=ffn_swiglu-22 op=(null)
[split-node] split=45 node=14 backend=OpenCL name=node_1464 op=ADD
[split-node] split=45 node=15 backend=OpenCL name=node_1465 op=ADD
[split-node] split=45 node=16 backend=OpenCL name=node_1466 op=ADD
[split-node] split=45 node=17 backend=OpenCL name=node_1467 op=ADD
[split-node] split=45 node=18 backend=OpenCL name=ffn_moe_out-22 op=ADD
[split-node] split=45 node=19 backend=OpenCL name=ffn_shexp-22 op=MUL_MAT
[split-node] split=45 node=20 backend=OpenCL name=ffn_out-22 op=ADD
[split-node] split=45 node=21 backend=OpenCL name=l_out-22 op=ADD
[split-node] split=45 node=22 backend=OpenCL name=norm-23 op=RMS_NORM
[split-node] split=45 node=23 backend=OpenCL name=attn_norm-23 op=MUL
[split-node] split=45 node=24 backend=OpenCL name=q-23 op=MUL_MAT
[split-node] split=45 node=25 backend=OpenCL name=q_pe-23 op=VIEW
[split-node] split=45 node=26 backend=OpenCL name=q_pe-23 op=ROPE
[split-node] split=45 node=27 backend=OpenCL name=q_nope-23 op=VIEW
[split-node] split=45 node=28 backend=OpenCL name=Qcur-23 op=CONCAT
[split-node] split=45 node=29 backend=OpenCL name=kv_cmpr_pe-23 op=MUL_MAT
[split-node] split=45 node=30 backend=OpenCL name=k_pe-23 op=VIEW
[split-node] split=45 node=31 backend=OpenCL name=k_pe-23 op=ROPE
[split-node] split=45 node=32 backend=OpenCL name=node_1482 op=REPEAT
[split-node] split=45 node=33 backend=OpenCL name=kv_cmpr-23 op=VIEW
[split-node] split=45 node=34 backend=OpenCL name=norm-23 op=RMS_NORM
[split-node] split=45 node=35 backend=OpenCL name=kv_cmpr-23 op=MUL
[split-node] split=45 node=36 backend=OpenCL name=kv-23 op=MUL_MAT
[split-node] split=45 node=37 backend=OpenCL name=k_nope_view-23 op=VIEW
[split-node] split=45 node=38 backend=OpenCL name=Kcur-23 op=CONCAT
[split-node] split=45 node=39 backend=OpenCL name=Vcur_view-23 op=VIEW
[split-node] split=45 node=40 backend=OpenCL name=Vcur_cont-23 op=CONT
[split-node] split=45 node=41 backend=OpenCL name=Kcur-23 (view) op=VIEW
[split-node] split=45 node=42 backend=OpenCL name=cache_k_l23 (view) op=SET_ROWS
[split-node] split=45 node=43 backend=OpenCL name=Vcur_cont-23 (view) op=VIEW
[split-node] split=45 node=44 backend=OpenCL name=cache_v_l23 (view) op=SET_ROWS
[split-node] split=45 node=45 backend=OpenCL name=Qcur-23 (view) op=VIEW
[split-node] split=45 node=46 backend=OpenCL name=Qcur-23 (view) (permuted) op=PERMUTE
[split-node] split=45 node=47 backend=OpenCL name=cache_k_l23 (view) op=VIEW
[split-node] split=45 node=48 backend=OpenCL name=cache_k_l23 (view) (permuted) op=PERMUTE
[split-node] split=45 node=49 backend=OpenCL name=cache_v_l23 (view) op=VIEW
[split-node] split=45 node=50 backend=OpenCL name=cache_v_l23 (view) (permuted) op=PERMUTE
[split-node] split=45 node=51 backend=OpenCL name=__fattn__-23 op=FLASH_ATTN_BACK
[split-node] split=45 node=52 backend=OpenCL name=kqv_out-23 op=RESHAPE
[split-node] split=45 node=53 backend=OpenCL name=node_1503 op=MUL_MAT
[split-node] split=45 node=54 backend=OpenCL name=ffn_inp-23 op=ADD
[split-node] split=45 node=55 backend=OpenCL name=norm-23 op=RMS_NORM
[split-node] split=45 node=56 backend=OpenCL name=ffn_norm-23 op=MUL
[split-node] split=45 node=57 backend=OpenCL name=ffn_moe_logits-23 op=MUL_MAT
[split-node] split=45 node=58 backend=OpenCL name=ffn_moe_probs-23 op=SOFT_MAX
[split-node] split=45 node=59 backend=OpenCL name=ffn_moe_probs-23 (reshaped) op=RESHAPE
[split-node] split=45 node=60 backend=OpenCL name=ffn_moe_argsort-23 op=ARGSORT
[split-node] split=45 node=61 backend=OpenCL name=ffn_moe_topk-23 op=VIEW
[split-node] split=45 node=62 backend=OpenCL name=ffn_moe_weights-23 op=GET_ROWS
[split-input] split=45 name=ffn_moe_weights_scaled-22 bytes=12288 backend_dst=OpenCL
[split-input] split=45 name=ffn_moe_topk-23 bytes=130840 backend_dst=OpenCL
[split-summary] id=46 backend=CPU nodes=2 inputs=1
[split-node] split=46 node=0 backend=CPU name=ffn_moe_weights_scaled-23 op=SCALE
[split-node] split=46 node=1 backend=OpenCL name=ffn_norm-23 (reshaped) op=RESHAPE
[split-input] split=46 name=ffn_moe_weights-23 bytes=12288 backend_dst=CPU
[split-summary] id=47 backend=OpenCL nodes=63 inputs=2
[split-node] split=47 node=0 backend=OpenCL name=ffn_moe_gate-23 op=MUL_MAT_ID
[split-node] split=47 node=1 backend=OpenCL name=ffn_moe_up-23 op=MUL_MAT_ID
[split-node] split=47 node=2 backend=OpenCL name=ffn_moe_weighted-23 op=(null)
[split-node] split=47 node=3 backend=OpenCL name=ffn_moe_down-23 op=MUL_MAT_ID
[split-node] split=47 node=4 backend=OpenCL name=node_1519 op=MUL
[split-node] split=47 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=47 node=6 backend=OpenCL name=node_1519 (view) op=VIEW
[split-node] split=47 node=7 backend=OpenCL name=node_1519 (view) op=VIEW
[split-node] split=47 node=8 backend=OpenCL name=node_1519 (view) op=VIEW
[split-node] split=47 node=9 backend=OpenCL name=node_1519 (view) op=VIEW
[split-node] split=47 node=10 backend=OpenCL name=node_1519 (view) op=VIEW
[split-node] split=47 node=11 backend=OpenCL name=ffn_gate-23 op=MUL_MAT
[split-node] split=47 node=12 backend=OpenCL name=ffn_up-23 op=MUL_MAT
[split-node] split=47 node=13 backend=OpenCL name=ffn_swiglu-23 op=(null)
[split-node] split=47 node=14 backend=OpenCL name=node_1529 op=ADD
[split-node] split=47 node=15 backend=OpenCL name=node_1530 op=ADD
[split-node] split=47 node=16 backend=OpenCL name=node_1531 op=ADD
[split-node] split=47 node=17 backend=OpenCL name=node_1532 op=ADD
[split-node] split=47 node=18 backend=OpenCL name=ffn_moe_out-23 op=ADD
[split-node] split=47 node=19 backend=OpenCL name=ffn_shexp-23 op=MUL_MAT
[split-node] split=47 node=20 backend=OpenCL name=ffn_out-23 op=ADD
[split-node] split=47 node=21 backend=OpenCL name=l_out-23 op=ADD
[split-node] split=47 node=22 backend=OpenCL name=norm-24 op=RMS_NORM
[split-node] split=47 node=23 backend=OpenCL name=attn_norm-24 op=MUL
[split-node] split=47 node=24 backend=OpenCL name=q-24 op=MUL_MAT
[split-node] split=47 node=25 backend=OpenCL name=q_pe-24 op=VIEW
[split-node] split=47 node=26 backend=OpenCL name=q_pe-24 op=ROPE
[split-node] split=47 node=27 backend=OpenCL name=q_nope-24 op=VIEW
[split-node] split=47 node=28 backend=OpenCL name=Qcur-24 op=CONCAT
[split-node] split=47 node=29 backend=OpenCL name=kv_cmpr_pe-24 op=MUL_MAT
[split-node] split=47 node=30 backend=OpenCL name=k_pe-24 op=VIEW
[split-node] split=47 node=31 backend=OpenCL name=k_pe-24 op=ROPE
[split-node] split=47 node=32 backend=OpenCL name=node_1547 op=REPEAT
[split-node] split=47 node=33 backend=OpenCL name=kv_cmpr-24 op=VIEW
[split-node] split=47 node=34 backend=OpenCL name=norm-24 op=RMS_NORM
[split-node] split=47 node=35 backend=OpenCL name=kv_cmpr-24 op=MUL
[split-node] split=47 node=36 backend=OpenCL name=kv-24 op=MUL_MAT
[split-node] split=47 node=37 backend=OpenCL name=k_nope_view-24 op=VIEW
[split-node] split=47 node=38 backend=OpenCL name=Kcur-24 op=CONCAT
[split-node] split=47 node=39 backend=OpenCL name=Vcur_view-24 op=VIEW
[split-node] split=47 node=40 backend=OpenCL name=Vcur_cont-24 op=CONT
[split-node] split=47 node=41 backend=OpenCL name=Kcur-24 (view) op=VIEW
[split-node] split=47 node=42 backend=OpenCL name=cache_k_l24 (view) op=SET_ROWS
[split-node] split=47 node=43 backend=OpenCL name=Vcur_cont-24 (view) op=VIEW
[split-node] split=47 node=44 backend=OpenCL name=cache_v_l24 (view) op=SET_ROWS
[split-node] split=47 node=45 backend=OpenCL name=Qcur-24 (view) op=VIEW
[split-node] split=47 node=46 backend=OpenCL name=Qcur-24 (view) (permuted) op=PERMUTE
[split-node] split=47 node=47 backend=OpenCL name=cache_k_l24 (view) op=VIEW
[split-node] split=47 node=48 backend=OpenCL name=cache_k_l24 (view) (permuted) op=PERMUTE
[split-node] split=47 node=49 backend=OpenCL name=cache_v_l24 (view) op=VIEW
[split-node] split=47 node=50 backend=OpenCL name=cache_v_l24 (view) (permuted) op=PERMUTE
[split-node] split=47 node=51 backend=OpenCL name=__fattn__-24 op=FLASH_ATTN_BACK
[split-node] split=47 node=52 backend=OpenCL name=kqv_out-24 op=RESHAPE
[split-node] split=47 node=53 backend=OpenCL name=node_1568 op=MUL_MAT
[split-node] split=47 node=54 backend=OpenCL name=ffn_inp-24 op=ADD
[split-node] split=47 node=55 backend=OpenCL name=norm-24 op=RMS_NORM
[split-node] split=47 node=56 backend=OpenCL name=ffn_norm-24 op=MUL
[split-node] split=47 node=57 backend=OpenCL name=ffn_moe_logits-24 op=MUL_MAT
[split-node] split=47 node=58 backend=OpenCL name=ffn_moe_probs-24 op=SOFT_MAX
[split-node] split=47 node=59 backend=OpenCL name=ffn_moe_probs-24 (reshaped) op=RESHAPE
[split-node] split=47 node=60 backend=OpenCL name=ffn_moe_argsort-24 op=ARGSORT
[split-node] split=47 node=61 backend=OpenCL name=ffn_moe_topk-24 op=VIEW
[split-node] split=47 node=62 backend=OpenCL name=ffn_moe_weights-24 op=GET_ROWS
[split-input] split=47 name=ffn_moe_weights_scaled-23 bytes=12288 backend_dst=OpenCL
[split-input] split=47 name=ffn_moe_topk-24 bytes=130840 backend_dst=OpenCL
[split-summary] id=48 backend=CPU nodes=2 inputs=1
[split-node] split=48 node=0 backend=CPU name=ffn_moe_weights_scaled-24 op=SCALE
[split-node] split=48 node=1 backend=OpenCL name=ffn_norm-24 (reshaped) op=RESHAPE
[split-input] split=48 name=ffn_moe_weights-24 bytes=12288 backend_dst=CPU
[split-summary] id=49 backend=OpenCL nodes=63 inputs=2
[split-node] split=49 node=0 backend=OpenCL name=ffn_moe_gate-24 op=MUL_MAT_ID
[split-node] split=49 node=1 backend=OpenCL name=ffn_moe_up-24 op=MUL_MAT_ID
[split-node] split=49 node=2 backend=OpenCL name=ffn_moe_weighted-24 op=(null)
[split-node] split=49 node=3 backend=OpenCL name=ffn_moe_down-24 op=MUL_MAT_ID
[split-node] split=49 node=4 backend=OpenCL name=node_1584 op=MUL
[split-node] split=49 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=49 node=6 backend=OpenCL name=node_1584 (view) op=VIEW
[split-node] split=49 node=7 backend=OpenCL name=node_1584 (view) op=VIEW
[split-node] split=49 node=8 backend=OpenCL name=node_1584 (view) op=VIEW
[split-node] split=49 node=9 backend=OpenCL name=node_1584 (view) op=VIEW
[split-node] split=49 node=10 backend=OpenCL name=node_1584 (view) op=VIEW
[split-node] split=49 node=11 backend=OpenCL name=ffn_gate-24 op=MUL_MAT
[split-node] split=49 node=12 backend=OpenCL name=ffn_up-24 op=MUL_MAT
[split-node] split=49 node=13 backend=OpenCL name=ffn_swiglu-24 op=(null)
[split-node] split=49 node=14 backend=OpenCL name=node_1594 op=ADD
[split-node] split=49 node=15 backend=OpenCL name=node_1595 op=ADD
[split-node] split=49 node=16 backend=OpenCL name=node_1596 op=ADD
[split-node] split=49 node=17 backend=OpenCL name=node_1597 op=ADD
[split-node] split=49 node=18 backend=OpenCL name=ffn_moe_out-24 op=ADD
[split-node] split=49 node=19 backend=OpenCL name=ffn_shexp-24 op=MUL_MAT
[split-node] split=49 node=20 backend=OpenCL name=ffn_out-24 op=ADD
[split-node] split=49 node=21 backend=OpenCL name=l_out-24 op=ADD
[split-node] split=49 node=22 backend=OpenCL name=norm-25 op=RMS_NORM
[split-node] split=49 node=23 backend=OpenCL name=attn_norm-25 op=MUL
[split-node] split=49 node=24 backend=OpenCL name=q-25 op=MUL_MAT
[split-node] split=49 node=25 backend=OpenCL name=q_pe-25 op=VIEW
[split-node] split=49 node=26 backend=OpenCL name=q_pe-25 op=ROPE
[split-node] split=49 node=27 backend=OpenCL name=q_nope-25 op=VIEW
[split-node] split=49 node=28 backend=OpenCL name=Qcur-25 op=CONCAT
[split-node] split=49 node=29 backend=OpenCL name=kv_cmpr_pe-25 op=MUL_MAT
[split-node] split=49 node=30 backend=OpenCL name=k_pe-25 op=VIEW
[split-node] split=49 node=31 backend=OpenCL name=k_pe-25 op=ROPE
[split-node] split=49 node=32 backend=OpenCL name=node_1612 op=REPEAT
[split-node] split=49 node=33 backend=OpenCL name=kv_cmpr-25 op=VIEW
[split-node] split=49 node=34 backend=OpenCL name=norm-25 op=RMS_NORM
[split-node] split=49 node=35 backend=OpenCL name=kv_cmpr-25 op=MUL
[split-node] split=49 node=36 backend=OpenCL name=kv-25 op=MUL_MAT
[split-node] split=49 node=37 backend=OpenCL name=k_nope_view-25 op=VIEW
[split-node] split=49 node=38 backend=OpenCL name=Kcur-25 op=CONCAT
[split-node] split=49 node=39 backend=OpenCL name=Vcur_view-25 op=VIEW
[split-node] split=49 node=40 backend=OpenCL name=Vcur_cont-25 op=CONT
[split-node] split=49 node=41 backend=OpenCL name=Kcur-25 (view) op=VIEW
[split-node] split=49 node=42 backend=OpenCL name=cache_k_l25 (view) op=SET_ROWS
[split-node] split=49 node=43 backend=OpenCL name=Vcur_cont-25 (view) op=VIEW
[split-node] split=49 node=44 backend=OpenCL name=cache_v_l25 (view) op=SET_ROWS
[split-node] split=49 node=45 backend=OpenCL name=Qcur-25 (view) op=VIEW
[split-node] split=49 node=46 backend=OpenCL name=Qcur-25 (view) (permuted) op=PERMUTE
[split-node] split=49 node=47 backend=OpenCL name=cache_k_l25 (view) op=VIEW
[split-node] split=49 node=48 backend=OpenCL name=cache_k_l25 (view) (permuted) op=PERMUTE
[split-node] split=49 node=49 backend=OpenCL name=cache_v_l25 (view) op=VIEW
[split-node] split=49 node=50 backend=OpenCL name=cache_v_l25 (view) (permuted) op=PERMUTE
[split-node] split=49 node=51 backend=OpenCL name=__fattn__-25 op=FLASH_ATTN_BACK
[split-node] split=49 node=52 backend=OpenCL name=kqv_out-25 op=RESHAPE
[split-node] split=49 node=53 backend=OpenCL name=node_1633 op=MUL_MAT
[split-node] split=49 node=54 backend=OpenCL name=ffn_inp-25 op=ADD
[split-node] split=49 node=55 backend=OpenCL name=norm-25 op=RMS_NORM
[split-node] split=49 node=56 backend=OpenCL name=ffn_norm-25 op=MUL
[split-node] split=49 node=57 backend=OpenCL name=ffn_moe_logits-25 op=MUL_MAT
[split-node] split=49 node=58 backend=OpenCL name=ffn_moe_probs-25 op=SOFT_MAX
[split-node] split=49 node=59 backend=OpenCL name=ffn_moe_probs-25 (reshaped) op=RESHAPE
[split-node] split=49 node=60 backend=OpenCL name=ffn_moe_argsort-25 op=ARGSORT
[split-node] split=49 node=61 backend=OpenCL name=ffn_moe_topk-25 op=VIEW
[split-node] split=49 node=62 backend=OpenCL name=ffn_moe_weights-25 op=GET_ROWS
[split-input] split=49 name=ffn_moe_weights_scaled-24 bytes=12288 backend_dst=OpenCL
[split-input] split=49 name=ffn_moe_topk-25 bytes=130840 backend_dst=OpenCL
[split-summary] id=50 backend=CPU nodes=2 inputs=1
[split-node] split=50 node=0 backend=CPU name=ffn_moe_weights_scaled-25 op=SCALE
[split-node] split=50 node=1 backend=OpenCL name=ffn_norm-25 (reshaped) op=RESHAPE
[split-input] split=50 name=ffn_moe_weights-25 bytes=12288 backend_dst=CPU
[split-summary] id=51 backend=OpenCL nodes=65 inputs=3
[split-node] split=51 node=0 backend=OpenCL name=ffn_moe_gate-25 op=MUL_MAT_ID
[split-node] split=51 node=1 backend=OpenCL name=ffn_moe_up-25 op=MUL_MAT_ID
[split-node] split=51 node=2 backend=OpenCL name=ffn_moe_weighted-25 op=(null)
[split-node] split=51 node=3 backend=OpenCL name=ffn_moe_down-25 op=MUL_MAT_ID
[split-node] split=51 node=4 backend=OpenCL name=node_1649 op=MUL
[split-node] split=51 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=51 node=6 backend=OpenCL name=node_1649 (view) op=VIEW
[split-node] split=51 node=7 backend=OpenCL name=node_1649 (view) op=VIEW
[split-node] split=51 node=8 backend=OpenCL name=node_1649 (view) op=VIEW
[split-node] split=51 node=9 backend=OpenCL name=node_1649 (view) op=VIEW
[split-node] split=51 node=10 backend=OpenCL name=node_1649 (view) op=VIEW
[split-node] split=51 node=11 backend=OpenCL name=ffn_gate-25 op=MUL_MAT
[split-node] split=51 node=12 backend=OpenCL name=ffn_up-25 op=MUL_MAT
[split-node] split=51 node=13 backend=OpenCL name=ffn_swiglu-25 op=(null)
[split-node] split=51 node=14 backend=OpenCL name=node_1659 op=ADD
[split-node] split=51 node=15 backend=OpenCL name=node_1660 op=ADD
[split-node] split=51 node=16 backend=OpenCL name=node_1661 op=ADD
[split-node] split=51 node=17 backend=OpenCL name=node_1662 op=ADD
[split-node] split=51 node=18 backend=OpenCL name=ffn_moe_out-25 op=ADD
[split-node] split=51 node=19 backend=OpenCL name=ffn_shexp-25 op=MUL_MAT
[split-node] split=51 node=20 backend=OpenCL name=ffn_out-25 op=ADD
[split-node] split=51 node=21 backend=OpenCL name=l_out-25 op=ADD
[split-node] split=51 node=22 backend=OpenCL name=norm-26 op=RMS_NORM
[split-node] split=51 node=23 backend=OpenCL name=attn_norm-26 op=MUL
[split-node] split=51 node=24 backend=OpenCL name=q-26 op=MUL_MAT
[split-node] split=51 node=25 backend=OpenCL name=q_pe-26 op=VIEW
[split-node] split=51 node=26 backend=OpenCL name=q_pe-26 op=ROPE
[split-node] split=51 node=27 backend=OpenCL name=q_nope-26 op=VIEW
[split-node] split=51 node=28 backend=OpenCL name=Qcur-26 op=CONCAT
[split-node] split=51 node=29 backend=OpenCL name=kv_cmpr_pe-26 op=MUL_MAT
[split-node] split=51 node=30 backend=OpenCL name=k_pe-26 op=VIEW
[split-node] split=51 node=31 backend=OpenCL name=k_pe-26 op=ROPE
[split-node] split=51 node=32 backend=OpenCL name=node_1677 op=REPEAT
[split-node] split=51 node=33 backend=OpenCL name=kv_cmpr-26 op=VIEW
[split-node] split=51 node=34 backend=OpenCL name=norm-26 op=RMS_NORM
[split-node] split=51 node=35 backend=OpenCL name=kv_cmpr-26 op=MUL
[split-node] split=51 node=36 backend=OpenCL name=kv-26 op=MUL_MAT
[split-node] split=51 node=37 backend=OpenCL name=k_nope_view-26 op=VIEW
[split-node] split=51 node=38 backend=OpenCL name=Kcur-26 op=CONCAT
[split-node] split=51 node=39 backend=OpenCL name=Vcur_view-26 op=VIEW
[split-node] split=51 node=40 backend=OpenCL name=Vcur_cont-26 op=CONT
[split-node] split=51 node=41 backend=OpenCL name=Kcur-26 (view) op=VIEW
[split-node] split=51 node=42 backend=OpenCL name=cache_k_l26 (view) op=SET_ROWS
[split-node] split=51 node=43 backend=OpenCL name=Vcur_cont-26 (view) op=VIEW
[split-node] split=51 node=44 backend=OpenCL name=cache_v_l26 (view) op=SET_ROWS
[split-node] split=51 node=45 backend=OpenCL name=Qcur-26 (view) op=VIEW
[split-node] split=51 node=46 backend=OpenCL name=Qcur-26 (view) (permuted) op=PERMUTE
[split-node] split=51 node=47 backend=OpenCL name=cache_k_l26 (view) op=VIEW
[split-node] split=51 node=48 backend=OpenCL name=cache_k_l26 (view) (permuted) op=PERMUTE
[split-node] split=51 node=49 backend=OpenCL name=cache_v_l26 (view) op=VIEW
[split-node] split=51 node=50 backend=OpenCL name=cache_v_l26 (view) (permuted) op=PERMUTE
[split-node] split=51 node=51 backend=OpenCL name=__fattn__-26 op=FLASH_ATTN_BACK
[split-node] split=51 node=52 backend=OpenCL name=kqv_out-26 op=RESHAPE
[split-node] split=51 node=53 backend=OpenCL name=node_1698 op=MUL_MAT
[split-node] split=51 node=54 backend=OpenCL name=node_1699 op=GET_ROWS
[split-node] split=51 node=55 backend=OpenCL name=node_1700 op=GET_ROWS
[split-node] split=51 node=56 backend=OpenCL name=ffn_inp-26 op=ADD
[split-node] split=51 node=57 backend=OpenCL name=norm-26 op=RMS_NORM
[split-node] split=51 node=58 backend=OpenCL name=ffn_norm-26 op=MUL
[split-node] split=51 node=59 backend=OpenCL name=ffn_moe_logits-26 op=MUL_MAT
[split-node] split=51 node=60 backend=OpenCL name=ffn_moe_probs-26 op=SOFT_MAX
[split-node] split=51 node=61 backend=OpenCL name=ffn_moe_probs-26 (reshaped) op=RESHAPE
[split-node] split=51 node=62 backend=OpenCL name=ffn_moe_argsort-26 op=ARGSORT
[split-node] split=51 node=63 backend=OpenCL name=ffn_moe_topk-26 op=VIEW
[split-node] split=51 node=64 backend=OpenCL name=ffn_moe_weights-26 op=GET_ROWS
[split-input] split=51 name=ffn_moe_weights_scaled-25 bytes=12288 backend_dst=OpenCL
[split-input] split=51 name=leaf_427 bytes=0 backend_dst=OpenCL
[split-input] split=51 name=ffn_moe_topk-26 bytes=0 backend_dst=OpenCL
[split-summary] id=52 backend=CPU nodes=2 inputs=1
[split-node] split=52 node=0 backend=CPU name=ffn_moe_weights_scaled-26 op=SCALE
[split-node] split=52 node=1 backend=OpenCL name=ffn_norm-26 (reshaped) op=RESHAPE
[split-input] split=52 name=ffn_moe_weights-26 bytes=0 backend_dst=CPU
[split-summary] id=53 backend=OpenCL nodes=25 inputs=1
[split-node] split=53 node=0 backend=OpenCL name=ffn_moe_gate-26 op=MUL_MAT_ID
[split-node] split=53 node=1 backend=OpenCL name=ffn_moe_up-26 op=MUL_MAT_ID
[split-node] split=53 node=2 backend=OpenCL name=ffn_moe_weighted-26 op=(null)
[split-node] split=53 node=3 backend=OpenCL name=ffn_moe_down-26 op=MUL_MAT_ID
[split-node] split=53 node=4 backend=OpenCL name=node_1716 op=MUL
[split-node] split=53 node=5 backend=OpenCL name= (view) op=VIEW
[split-node] split=53 node=6 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=53 node=7 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=53 node=8 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=53 node=9 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=53 node=10 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=53 node=11 backend=OpenCL name=ffn_gate-26 op=MUL_MAT
[split-node] split=53 node=12 backend=OpenCL name=ffn_up-26 op=MUL_MAT
[split-node] split=53 node=13 backend=OpenCL name=ffn_swiglu-26 op=(null)
[split-node] split=53 node=14 backend=OpenCL name=node_1726 op=ADD
[split-node] split=53 node=15 backend=OpenCL name=node_1727 op=ADD
[split-node] split=53 node=16 backend=OpenCL name=node_1728 op=ADD
[split-node] split=53 node=17 backend=OpenCL name=node_1729 op=ADD
[split-node] split=53 node=18 backend=OpenCL name=ffn_moe_out-26 op=ADD
[split-node] split=53 node=19 backend=OpenCL name=ffn_shexp-26 op=MUL_MAT
[split-node] split=53 node=20 backend=OpenCL name=ffn_out-26 op=ADD
[split-node] split=53 node=21 backend=OpenCL name=l_out-26 op=ADD
[split-node] split=53 node=22 backend=OpenCL name=norm op=RMS_NORM
[split-node] split=53 node=23 backend=OpenCL name=result_norm op=MUL
[split-node] split=53 node=24 backend=OpenCL name=result_output op=MUL_MAT