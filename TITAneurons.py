from brian2 import *
import matplotlib.pyplot as plt

# TI, TA 해보기

def sim(ax_vm, ax_w, ax_vm_w, parameters):
    """
    simulate with parameters and plot to axes
    """

    # taken from Touboul_Brette_2008
    eqs = """
    dvm/dt = (g_l*(e_l - vm) + g_l*d_t*exp((vm-v_t)/d_t) + i_stim - w)/c_m : volt   # 뉴런 막전위 변화
    dw/dt  = (a*(vm - e_l) - w)/tau_w : amp #                                       # 적응전류 변화
    """

    neuron = NeuronGroup(
        1,
        model=eqs,
        threshold="vm > t_f ",
        reset="vm = v_r; w += b",
        method="euler",
        namespace=parameters,
    )

    neuron.vm = parameters["e_l"]
    neuron.w = 0            # 뉴런의 초기 적응 전류 : 0

    states = StateMonitor(neuron, ["vm", "w"], record=True, when="thresholds")   #막전위와 적응 전류를 기록

    defaultclock.dt = 0.1 * ms # 시뮬레이션의 시간 간격
    run(0.6 * second) # 0.6초 동안 시뮬레이션을 실행

    # clip membrane voltages to threshold (0 mV)
    vms = np.clip(states[0].vm / mV, a_min=None, a_max=0)

    ax_vm.plot(states[0].t / ms, vms)   # 막전위를 시간에 따라 그래프
    ax_w.plot(states[0].t / ms, states[0].w / nA)   # 적응 전류를 시간에 따라 그래프
    ax_vm_w.plot(vms, states[0].w / nA) # 막전위, 적응 전류 함께 그래프

    ax_w.sharex(ax_vm) # ax_w와 ax_vm의 x축을 공유
    ax_vm.tick_params(labelbottom=False) # ax_vm의 x축 레이블 숨김

    ax_vm.set_ylabel("V [mV]")

    ax_w.set_xlabel("t [ms]")
    ax_w.set_ylabel("w [nA]")

    ax_vm_w.set_xlabel("V [mV]")
    ax_vm_w.set_ylabel("w [nA]")

    ax_vm_w.yaxis.tick_right() # ax_vm_w의 y축을 오른쪽으로 이동
    ax_vm_w.yaxis.set_label_position("right") # ax_vm_w의 y축 레이블을 오른쪽으로 설정

# TI, TA neurons parameters
patterns = {
    "TI spiking": {
        "c_m": 40 * pF, 
        "g_l": 1 * nS, 
        "e_l": -55.1 * mV, 
        "v_t": -54.7 * mV, 
        "d_t": 1.7 * mV, ####2.0 * mV,
        "a": 2.5 * nS, 
        "tau_w": 20.0 * ms, 
        "b": 70 * pA, 
        "v_r": -60.0 * mV, 
        "i_stim": 12 * pA, 
        "t_f": 15 * mV,
    },
    
    "TA spiking": {
        "c_m": 60 * pF, 
        "g_l": 1 * nS, 
        "e_l": -55.1 * mV, 
        "v_t": -54.7 * mV, 
        "d_t": 2.55 * mV, ####2.0 * mV,
        "a": 2.5 * nS, 
        "tau_w": 20.0 * ms, 
        "b": 105 * pA, 
        "v_r": -60.0 * mV, 
        "i_stim": 1 * pA, 
        "t_f": 15 * mV,

    },
}
# loop over all patterns and plot
for pattern, parameters in patterns.items():

    fig = plt.figure(figsize=(10, 5))
    fig.suptitle(pattern)
    gs = fig.add_gridspec(2, 2)

    ax_vm = fig.add_subplot(gs[0, 0])
    ax_w = fig.add_subplot(gs[1, 0])
    ax_vm_w = fig.add_subplot(gs[:, 1])

    sim(ax_vm, ax_w, ax_vm_w, parameters)
plt.show()