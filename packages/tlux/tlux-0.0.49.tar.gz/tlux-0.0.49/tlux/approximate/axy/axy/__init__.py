'''This Python code is an automatically generated wrapper
for Fortran code made by 'fmodpy'. The original documentation
for the Fortran source code follows.

!
! To start linter for Emacs:
!   M-x lsp
!   M-x lsp-diagnostics-mode
!     for some reason this needs to be done for error highlighting
!   C-c ! n
!     next error or warning
!   C-c ! p
!     previous error or warning
!   M-x magit-status
!     look at all changes in current commit
!
! TODO:
!
! - Add "chords" that enables parallel additive XY models.
!
! - "Dynamic data normalization" default to 4 when batch size is smaller than all data,
!   includes updates to zero mean, unit variance, pca-for-covariance included in the
!   gradient calculation exactly as is done for the AY values.
!
! - Add incremental checks (and updates?) to the normalization matrices generated from a batch
!   of data, since the normalizations determined might be "bad". Could use a very slow sliding
!   average so that value will only update in the face of large data shifts. Could compute the
!   gradient towards the true PCA by doing one power iteration, as well as the gradient towards
!   componentwise zero mean and unit variance.
!
! - Track aggregate output state (either in X or Y) for model conditioning steps so that
!   can be use to correctly normalize the values coming out of the aggregate model for
!   componentwise zero mean and unit variance.
!
! - Add a parameter PARTIAL_STEPS that determines how many steps are included in
!   the partial aggregation process. This can be used to short-circuit doing all
!   possible subset sizes, instead only doing subsets of well-spaced sizes.
!   Specifically, those steps should traverse including all comparisons between
!   increasingly more elements (so progressing as ~x**2).
!
! - Pull normalization code out and have it be called separately from 'FIT'.
!   Goal is to achieve near-zero inefficiencies for doing a few steps at a time in
!   Python (allowing for easier cancellation, progress updates, checkpoints, ...).
!
! - Rotate out the points that have the lowest expected change in error when batching.
!
! - Update CONDITION_MODEL to:
!    multiply the 2-norm of output weights by values before orthogonalization
!    compress basis weights with linear regression when rank deficiency is detected
!    reinitialize basis functions randomly at first, metric PCA best
!    sum the number of times a component had no rank across threads
!    swap weights for the no-rank components to the back
!    swap no-rank state component values into contiguous memory at back
!    linearly regress the kept-components onto the next-layer dropped difference
!    compute the first no-rank principal components of the gradient, store in droped slots
!    regress previous layer onto the gradient components
!    fill any remaining nodes (if not enough from gradient) with "uncaptured" principal components
!    set new shift terms as the best of 5 well spaced values in [-1,1], or random given no order
!
! - Check if OMP TARGET actually sends code to a different device.
! - Experiment with 'OMP TARGET TEAMS DISTRIBUTE PARALLEL' to see if it uses GPU correctly.
!
! - Run some tests to determine how weights should be updated on conditioning
!   to not change the output of the model *at all*, and similarly update the
!   gradient estimates to reflect those changes as well (might have to reset gradient).
!
! - Verify that the *condition model* operation correctly updates the gradient
!   related variables (mean and curvature). (resets back to initialization)
!
! - Make model conditioning use the same work space as evaluation (where possible).
! - Implement and test Fortran native version of GEMM (manual DO loop).
! - Implement and test Fortran native version of SYRK (manual DO loop).
!
! ---------------------------------------------------------------------------
!
! NOTES:
!
! - When conditioning the model, the multipliers applied to the weight matrices
!   can affect the model gradient in nonlinear (difficult to predict) ways.
!
! - When taking adaptive optimization steps, the current architecture takes steps
!   and then projects back onto the feasible region (of the optimization space).
!   The projection is not incorporated directly into the steps, so it is possible
!   for these two operations to "fight" each other. This is ignored.
!

! An aggregator and fixed piecewise linear regression model.
'''

import os
import ctypes
import platform
import numpy

# --------------------------------------------------------------------
#               CONFIGURATION
# 
_verbose = True
_fort_compiler = "gfortran"
_shared_object_name = "axy." + platform.machine() + ".so"
_this_directory = os.path.dirname(os.path.abspath(__file__))
_path_to_lib = os.path.join(_this_directory, _shared_object_name)
_compile_options = ['-fPIC', '-shared', '-O3', '-lblas', '-llapack', '-fopenmp']
_ordered_dependencies = ['pcg32.f90', 'axy_profiler.f90', 'axy_random.f90', 'axy_matrix_operations.f90', 'axy_sort_and_select.f90', 'axy.f90', 'axy_c_wrapper.f90']
_symbol_files = []# 
# --------------------------------------------------------------------
#               AUTO-COMPILING
#
# Try to import the prerequisite symbols for the compiled code.
for _ in _symbol_files:
    _ = ctypes.CDLL(os.path.join(_this_directory, _), mode=ctypes.RTLD_GLOBAL)
# Try to import the existing object. If that fails, recompile and then try.
try:
    # Check to see if the source files have been modified and a recompilation is needed.
    if (max(max([0]+[os.path.getmtime(os.path.realpath(os.path.join(_this_directory,_))) for _ in _symbol_files]),
            max([0]+[os.path.getmtime(os.path.realpath(os.path.join(_this_directory,_))) for _ in _ordered_dependencies]))
        > os.path.getmtime(_path_to_lib)):
        print()
        print("WARNING: Recompiling because the modification time of a source file is newer than the library.", flush=True)
        print()
        if os.path.exists(_path_to_lib):
            os.remove(_path_to_lib)
        raise NotImplementedError(f"The newest library code has not been compiled.")
    # Import the library.
    clib = ctypes.CDLL(_path_to_lib)
except:
    # Remove the shared object if it exists, because it is faulty.
    if os.path.exists(_shared_object_name):
        os.remove(_shared_object_name)
    # Compile a new shared object.
    _command = [_fort_compiler] + _ordered_dependencies + _compile_options + ["-o", _shared_object_name]
    if _verbose:
        print("Running system command with arguments")
        print("  ", " ".join(_command))
    # Run the compilation command.
    import subprocess
    subprocess.check_call(_command, cwd=_this_directory)
    # Import the shared object file as a C library with ctypes.
    clib = ctypes.CDLL(_path_to_lib)
# --------------------------------------------------------------------


# This defines a C structure that can be used to hold this defined type.
class PROFILE_ENTRY(ctypes.Structure):
    # (name, ctype) fields for this structure.
    _fields_ = [("wall_time", ctypes.c_double), ("cpu_time", ctypes.c_double), ("call_count", ctypes.c_long), ("start_wall_time", ctypes.c_double), ("start_cpu_time", ctypes.c_double)]
    # Define an "__init__" that can take a class or keyword arguments as input.
    def __init__(self, value=0, **kwargs):
        # From whatever object (or dictionary) was given, assign internal values.
        self.wall_time = kwargs.get("wall_time", getattr(value, "wall_time", value))
        self.cpu_time = kwargs.get("cpu_time", getattr(value, "cpu_time", value))
        self.call_count = kwargs.get("call_count", getattr(value, "call_count", value))
        self.start_wall_time = kwargs.get("start_wall_time", getattr(value, "start_wall_time", value))
        self.start_cpu_time = kwargs.get("start_cpu_time", getattr(value, "start_cpu_time", value))
    # Define a "__str__" that produces a legible summary of this type.
    def __str__(self):
        s = []
        for (n, t) in self._fields_:
            s.append( n + "=" + str(getattr(self,n)) )
        return "PROFILE_ENTRY[" + ", ".join(s) + "]"
    # Define an "__eq__" method that checks equality of all fields.
    def __eq__(self, other):
        for (n, t) in self._fields_:
            if (getattr(self, n) != getattr(other, n, None)):
                return False
        return True



class axy:
    ''''''
    
    # This defines a C structure that can be used to hold this defined type.
    class MODEL_CONFIG(ctypes.Structure):
        # (name, ctype) fields for this structure.
        _fields_ = [("adn", ctypes.c_int), ("ade", ctypes.c_int), ("ane", ctypes.c_int), ("ads", ctypes.c_int), ("ans", ctypes.c_int), ("anc", ctypes.c_int), ("ado", ctypes.c_int), ("adi", ctypes.c_int), ("adso", ctypes.c_int), ("mdn", ctypes.c_int), ("mde", ctypes.c_int), ("mne", ctypes.c_int), ("mds", ctypes.c_int), ("mns", ctypes.c_int), ("mnc", ctypes.c_int), ("mdo", ctypes.c_int), ("mdi", ctypes.c_int), ("mdso", ctypes.c_int), ("doe", ctypes.c_int), ("noe", ctypes.c_int), ("don", ctypes.c_int), ("do", ctypes.c_int), ("total_size", ctypes.c_long), ("num_vars", ctypes.c_long), ("asev", ctypes.c_long), ("aeev", ctypes.c_long), ("asiv", ctypes.c_long), ("aeiv", ctypes.c_long), ("asis", ctypes.c_long), ("aeis", ctypes.c_long), ("assv", ctypes.c_long), ("aesv", ctypes.c_long), ("asss", ctypes.c_long), ("aess", ctypes.c_long), ("asov", ctypes.c_long), ("aeov", ctypes.c_long), ("msev", ctypes.c_long), ("meev", ctypes.c_long), ("msiv", ctypes.c_long), ("meiv", ctypes.c_long), ("msis", ctypes.c_long), ("meis", ctypes.c_long), ("mssv", ctypes.c_long), ("mesv", ctypes.c_long), ("msss", ctypes.c_long), ("mess", ctypes.c_long), ("msov", ctypes.c_long), ("meov", ctypes.c_long), ("osev", ctypes.c_long), ("oeev", ctypes.c_long), ("aiss", ctypes.c_long), ("aise", ctypes.c_long), ("aoss", ctypes.c_long), ("aose", ctypes.c_long), ("aoms", ctypes.c_long), ("aome", ctypes.c_long), ("aims", ctypes.c_long), ("aime", ctypes.c_long), ("aecs", ctypes.c_long), ("aece", ctypes.c_long), ("miss", ctypes.c_long), ("mise", ctypes.c_long), ("moss", ctypes.c_long), ("mose", ctypes.c_long), ("mims", ctypes.c_long), ("mime", ctypes.c_long), ("moms", ctypes.c_long), ("mome", ctypes.c_long), ("mecs", ctypes.c_long), ("mece", ctypes.c_long), ("oecs", ctypes.c_long), ("oece", ctypes.c_long), ("discontinuity", ctypes.c_float), ("category_gap", ctypes.c_float), ("min_agg_weight", ctypes.c_float), ("min_step_factor", ctypes.c_float), ("step_factor", ctypes.c_float), ("max_step_factor", ctypes.c_float), ("min_curv_component", ctypes.c_float), ("max_curv_component", ctypes.c_float), ("max_step_component", ctypes.c_float), ("faster_rate", ctypes.c_float), ("slower_rate", ctypes.c_float), ("min_update_ratio", ctypes.c_float), ("update_ratio_step", ctypes.c_float), ("step_mean_change", ctypes.c_float), ("step_curv_change", ctypes.c_float), ("step_ay_change", ctypes.c_float), ("step_emb_change", ctypes.c_float), ("initial_curv_estimate", ctypes.c_float), ("mse_upper_limit", ctypes.c_float), ("steps_taken", ctypes.c_long), ("min_steps_to_stability", ctypes.c_long), ("max_batch", ctypes.c_long), ("num_threads", ctypes.c_long), ("data_condition_frequency", ctypes.c_long), ("model_condition_frequency", ctypes.c_long), ("log_grad_norm_frequency", ctypes.c_long), ("rank_check_frequency", ctypes.c_long), ("num_to_update", ctypes.c_long), ("interrupt_delay_sec", ctypes.c_long), ("basis_replacement", ctypes.c_bool), ("keep_best", ctypes.c_bool), ("early_stop", ctypes.c_bool), ("reshuffle", ctypes.c_bool), ("pairwise_aggregation", ctypes.c_bool), ("partial_aggregation", ctypes.c_bool), ("ordered_aggregation", ctypes.c_bool), ("ax_normalized", ctypes.c_bool), ("rescale_ax", ctypes.c_bool), ("axi_normalized", ctypes.c_bool), ("ay_normalized", ctypes.c_bool), ("x_normalized", ctypes.c_bool), ("rescale_x", ctypes.c_bool), ("xi_normalized", ctypes.c_bool), ("y_normalized", ctypes.c_bool), ("rescale_y", ctypes.c_bool), ("yi_normalized", ctypes.c_bool), ("encode_scaling", ctypes.c_bool), ("normalize", ctypes.c_bool), ("needs_shifting", ctypes.c_bool), ("needs_cleaning", ctypes.c_bool), ("needs_scaling", ctypes.c_bool), ("rwork_size", ctypes.c_long), ("iwork_size", ctypes.c_long), ("lwork_size", ctypes.c_long), ("na", ctypes.c_long), ("nat", ctypes.c_long), ("nm", ctypes.c_long), ("nms", ctypes.c_long), ("nmt", ctypes.c_long), ("i_next", ctypes.c_long), ("i_step", ctypes.c_long), ("i_mult", ctypes.c_long), ("i_mod", ctypes.c_long), ("i_iter", ctypes.c_long), ("smg", ctypes.c_long), ("emg", ctypes.c_long), ("smgm", ctypes.c_long), ("emgm", ctypes.c_long), ("smgc", ctypes.c_long), ("emgc", ctypes.c_long), ("sbm", ctypes.c_long), ("ebm", ctypes.c_long), ("saxb", ctypes.c_long), ("eaxb", ctypes.c_long), ("say", ctypes.c_long), ("eay", ctypes.c_long), ("smxb", ctypes.c_long), ("emxb", ctypes.c_long), ("smyb", ctypes.c_long), ("emyb", ctypes.c_long), ("sag", ctypes.c_long), ("eag", ctypes.c_long), ("saet", ctypes.c_long), ("eaet", ctypes.c_long), ("saxs", ctypes.c_long), ("eaxs", ctypes.c_long), ("saxg", ctypes.c_long), ("eaxg", ctypes.c_long), ("sayg", ctypes.c_long), ("eayg", ctypes.c_long), ("sxg", ctypes.c_long), ("exg", ctypes.c_long), ("smet", ctypes.c_long), ("emet", ctypes.c_long), ("smxs", ctypes.c_long), ("emxs", ctypes.c_long), ("smxg", ctypes.c_long), ("emxg", ctypes.c_long), ("soet", ctypes.c_long), ("eoet", ctypes.c_long), ("seos", ctypes.c_long), ("eeos", ctypes.c_long), ("seog", ctypes.c_long), ("eeog", ctypes.c_long), ("syg", ctypes.c_long), ("eyg", ctypes.c_long), ("saxis", ctypes.c_long), ("eaxis", ctypes.c_long), ("saxir", ctypes.c_long), ("eaxir", ctypes.c_long), ("smxis", ctypes.c_long), ("emxis", ctypes.c_long), ("smxir", ctypes.c_long), ("emxir", ctypes.c_long), ("soxis", ctypes.c_long), ("eoxis", ctypes.c_long), ("soxir", ctypes.c_long), ("eoxir", ctypes.c_long), ("sal", ctypes.c_long), ("eal", ctypes.c_long), ("sml", ctypes.c_long), ("eml", ctypes.c_long), ("sast", ctypes.c_long), ("east", ctypes.c_long), ("smst", ctypes.c_long), ("emst", ctypes.c_long), ("saxi", ctypes.c_long), ("eaxi", ctypes.c_long), ("smxi", ctypes.c_long), ("emxi", ctypes.c_long), ("soxi", ctypes.c_long), ("eoxi", ctypes.c_long), ("ssb", ctypes.c_long), ("esb", ctypes.c_long), ("sao", ctypes.c_long), ("eao", ctypes.c_long), ("smo", ctypes.c_long), ("emo", ctypes.c_long), ("sui", ctypes.c_long), ("eui", ctypes.c_long), ("wint", ctypes.c_long), ("cint", ctypes.c_long), ("wfit", ctypes.c_long), ("cfit", ctypes.c_long), ("wnrm", ctypes.c_long), ("cnrm", ctypes.c_long), ("wgen", ctypes.c_long), ("cgen", ctypes.c_long), ("wemb", ctypes.c_long), ("cemb", ctypes.c_long), ("wevl", ctypes.c_long), ("cevl", ctypes.c_long), ("wgrd", ctypes.c_long), ("cgrd", ctypes.c_long), ("wrat", ctypes.c_long), ("crat", ctypes.c_long), ("wopt", ctypes.c_long), ("copt", ctypes.c_long), ("wcon", ctypes.c_long), ("ccon", ctypes.c_long), ("wrec", ctypes.c_long), ("crec", ctypes.c_long), ("wenc", ctypes.c_long), ("cenc", ctypes.c_long), ("fit_mse", ctypes.c_float), ("fit_prev_mse", ctypes.c_float), ("fit_best_mse", ctypes.c_float), ("fit_step_mean_remain", ctypes.c_float), ("fit_step_curv_remain", ctypes.c_float), ("fit_total_eval_rank", ctypes.c_int), ("fit_total_grad_rank", ctypes.c_int), ("fit_normalize", ctypes.c_bool), ("fit_step", ctypes.c_long), ("fit_min_to_update", ctypes.c_long), ("fit_last_interrupt_time", ctypes.c_long), ("fit_wait_time", ctypes.c_long), ("fit_total_rank", ctypes.c_long), ("fit_ns", ctypes.c_long), ("fit_nt", ctypes.c_long)]
        # Define an "__init__" that can take a class or keyword arguments as input.
        def __init__(self, value=0, **kwargs):
            # From whatever object (or dictionary) was given, assign internal values.
            self.adn = kwargs.get("adn", getattr(value, "adn", value))
            self.ade = kwargs.get("ade", getattr(value, "ade", value))
            self.ane = kwargs.get("ane", getattr(value, "ane", value))
            self.ads = kwargs.get("ads", getattr(value, "ads", value))
            self.ans = kwargs.get("ans", getattr(value, "ans", value))
            self.anc = kwargs.get("anc", getattr(value, "anc", value))
            self.ado = kwargs.get("ado", getattr(value, "ado", value))
            self.adi = kwargs.get("adi", getattr(value, "adi", value))
            self.adso = kwargs.get("adso", getattr(value, "adso", value))
            self.mdn = kwargs.get("mdn", getattr(value, "mdn", value))
            self.mde = kwargs.get("mde", getattr(value, "mde", value))
            self.mne = kwargs.get("mne", getattr(value, "mne", value))
            self.mds = kwargs.get("mds", getattr(value, "mds", value))
            self.mns = kwargs.get("mns", getattr(value, "mns", value))
            self.mnc = kwargs.get("mnc", getattr(value, "mnc", value))
            self.mdo = kwargs.get("mdo", getattr(value, "mdo", value))
            self.mdi = kwargs.get("mdi", getattr(value, "mdi", value))
            self.mdso = kwargs.get("mdso", getattr(value, "mdso", value))
            self.doe = kwargs.get("doe", getattr(value, "doe", value))
            self.noe = kwargs.get("noe", getattr(value, "noe", value))
            self.don = kwargs.get("don", getattr(value, "don", value))
            self.do = kwargs.get("do", getattr(value, "do", value))
            self.total_size = kwargs.get("total_size", getattr(value, "total_size", value))
            self.num_vars = kwargs.get("num_vars", getattr(value, "num_vars", value))
            self.asev = kwargs.get("asev", getattr(value, "asev", value))
            self.aeev = kwargs.get("aeev", getattr(value, "aeev", value))
            self.asiv = kwargs.get("asiv", getattr(value, "asiv", value))
            self.aeiv = kwargs.get("aeiv", getattr(value, "aeiv", value))
            self.asis = kwargs.get("asis", getattr(value, "asis", value))
            self.aeis = kwargs.get("aeis", getattr(value, "aeis", value))
            self.assv = kwargs.get("assv", getattr(value, "assv", value))
            self.aesv = kwargs.get("aesv", getattr(value, "aesv", value))
            self.asss = kwargs.get("asss", getattr(value, "asss", value))
            self.aess = kwargs.get("aess", getattr(value, "aess", value))
            self.asov = kwargs.get("asov", getattr(value, "asov", value))
            self.aeov = kwargs.get("aeov", getattr(value, "aeov", value))
            self.msev = kwargs.get("msev", getattr(value, "msev", value))
            self.meev = kwargs.get("meev", getattr(value, "meev", value))
            self.msiv = kwargs.get("msiv", getattr(value, "msiv", value))
            self.meiv = kwargs.get("meiv", getattr(value, "meiv", value))
            self.msis = kwargs.get("msis", getattr(value, "msis", value))
            self.meis = kwargs.get("meis", getattr(value, "meis", value))
            self.mssv = kwargs.get("mssv", getattr(value, "mssv", value))
            self.mesv = kwargs.get("mesv", getattr(value, "mesv", value))
            self.msss = kwargs.get("msss", getattr(value, "msss", value))
            self.mess = kwargs.get("mess", getattr(value, "mess", value))
            self.msov = kwargs.get("msov", getattr(value, "msov", value))
            self.meov = kwargs.get("meov", getattr(value, "meov", value))
            self.osev = kwargs.get("osev", getattr(value, "osev", value))
            self.oeev = kwargs.get("oeev", getattr(value, "oeev", value))
            self.aiss = kwargs.get("aiss", getattr(value, "aiss", value))
            self.aise = kwargs.get("aise", getattr(value, "aise", value))
            self.aoss = kwargs.get("aoss", getattr(value, "aoss", value))
            self.aose = kwargs.get("aose", getattr(value, "aose", value))
            self.aoms = kwargs.get("aoms", getattr(value, "aoms", value))
            self.aome = kwargs.get("aome", getattr(value, "aome", value))
            self.aims = kwargs.get("aims", getattr(value, "aims", value))
            self.aime = kwargs.get("aime", getattr(value, "aime", value))
            self.aecs = kwargs.get("aecs", getattr(value, "aecs", value))
            self.aece = kwargs.get("aece", getattr(value, "aece", value))
            self.miss = kwargs.get("miss", getattr(value, "miss", value))
            self.mise = kwargs.get("mise", getattr(value, "mise", value))
            self.moss = kwargs.get("moss", getattr(value, "moss", value))
            self.mose = kwargs.get("mose", getattr(value, "mose", value))
            self.mims = kwargs.get("mims", getattr(value, "mims", value))
            self.mime = kwargs.get("mime", getattr(value, "mime", value))
            self.moms = kwargs.get("moms", getattr(value, "moms", value))
            self.mome = kwargs.get("mome", getattr(value, "mome", value))
            self.mecs = kwargs.get("mecs", getattr(value, "mecs", value))
            self.mece = kwargs.get("mece", getattr(value, "mece", value))
            self.oecs = kwargs.get("oecs", getattr(value, "oecs", value))
            self.oece = kwargs.get("oece", getattr(value, "oece", value))
            self.discontinuity = kwargs.get("discontinuity", getattr(value, "discontinuity", value))
            self.category_gap = kwargs.get("category_gap", getattr(value, "category_gap", value))
            self.min_agg_weight = kwargs.get("min_agg_weight", getattr(value, "min_agg_weight", value))
            self.min_step_factor = kwargs.get("min_step_factor", getattr(value, "min_step_factor", value))
            self.step_factor = kwargs.get("step_factor", getattr(value, "step_factor", value))
            self.max_step_factor = kwargs.get("max_step_factor", getattr(value, "max_step_factor", value))
            self.min_curv_component = kwargs.get("min_curv_component", getattr(value, "min_curv_component", value))
            self.max_curv_component = kwargs.get("max_curv_component", getattr(value, "max_curv_component", value))
            self.max_step_component = kwargs.get("max_step_component", getattr(value, "max_step_component", value))
            self.faster_rate = kwargs.get("faster_rate", getattr(value, "faster_rate", value))
            self.slower_rate = kwargs.get("slower_rate", getattr(value, "slower_rate", value))
            self.min_update_ratio = kwargs.get("min_update_ratio", getattr(value, "min_update_ratio", value))
            self.update_ratio_step = kwargs.get("update_ratio_step", getattr(value, "update_ratio_step", value))
            self.step_mean_change = kwargs.get("step_mean_change", getattr(value, "step_mean_change", value))
            self.step_curv_change = kwargs.get("step_curv_change", getattr(value, "step_curv_change", value))
            self.step_ay_change = kwargs.get("step_ay_change", getattr(value, "step_ay_change", value))
            self.step_emb_change = kwargs.get("step_emb_change", getattr(value, "step_emb_change", value))
            self.initial_curv_estimate = kwargs.get("initial_curv_estimate", getattr(value, "initial_curv_estimate", value))
            self.mse_upper_limit = kwargs.get("mse_upper_limit", getattr(value, "mse_upper_limit", value))
            self.steps_taken = kwargs.get("steps_taken", getattr(value, "steps_taken", value))
            self.min_steps_to_stability = kwargs.get("min_steps_to_stability", getattr(value, "min_steps_to_stability", value))
            self.max_batch = kwargs.get("max_batch", getattr(value, "max_batch", value))
            self.num_threads = kwargs.get("num_threads", getattr(value, "num_threads", value))
            self.data_condition_frequency = kwargs.get("data_condition_frequency", getattr(value, "data_condition_frequency", value))
            self.model_condition_frequency = kwargs.get("model_condition_frequency", getattr(value, "model_condition_frequency", value))
            self.log_grad_norm_frequency = kwargs.get("log_grad_norm_frequency", getattr(value, "log_grad_norm_frequency", value))
            self.rank_check_frequency = kwargs.get("rank_check_frequency", getattr(value, "rank_check_frequency", value))
            self.num_to_update = kwargs.get("num_to_update", getattr(value, "num_to_update", value))
            self.interrupt_delay_sec = kwargs.get("interrupt_delay_sec", getattr(value, "interrupt_delay_sec", value))
            self.basis_replacement = kwargs.get("basis_replacement", getattr(value, "basis_replacement", value))
            self.keep_best = kwargs.get("keep_best", getattr(value, "keep_best", value))
            self.early_stop = kwargs.get("early_stop", getattr(value, "early_stop", value))
            self.reshuffle = kwargs.get("reshuffle", getattr(value, "reshuffle", value))
            self.pairwise_aggregation = kwargs.get("pairwise_aggregation", getattr(value, "pairwise_aggregation", value))
            self.partial_aggregation = kwargs.get("partial_aggregation", getattr(value, "partial_aggregation", value))
            self.ordered_aggregation = kwargs.get("ordered_aggregation", getattr(value, "ordered_aggregation", value))
            self.ax_normalized = kwargs.get("ax_normalized", getattr(value, "ax_normalized", value))
            self.rescale_ax = kwargs.get("rescale_ax", getattr(value, "rescale_ax", value))
            self.axi_normalized = kwargs.get("axi_normalized", getattr(value, "axi_normalized", value))
            self.ay_normalized = kwargs.get("ay_normalized", getattr(value, "ay_normalized", value))
            self.x_normalized = kwargs.get("x_normalized", getattr(value, "x_normalized", value))
            self.rescale_x = kwargs.get("rescale_x", getattr(value, "rescale_x", value))
            self.xi_normalized = kwargs.get("xi_normalized", getattr(value, "xi_normalized", value))
            self.y_normalized = kwargs.get("y_normalized", getattr(value, "y_normalized", value))
            self.rescale_y = kwargs.get("rescale_y", getattr(value, "rescale_y", value))
            self.yi_normalized = kwargs.get("yi_normalized", getattr(value, "yi_normalized", value))
            self.encode_scaling = kwargs.get("encode_scaling", getattr(value, "encode_scaling", value))
            self.normalize = kwargs.get("normalize", getattr(value, "normalize", value))
            self.needs_shifting = kwargs.get("needs_shifting", getattr(value, "needs_shifting", value))
            self.needs_cleaning = kwargs.get("needs_cleaning", getattr(value, "needs_cleaning", value))
            self.needs_scaling = kwargs.get("needs_scaling", getattr(value, "needs_scaling", value))
            self.rwork_size = kwargs.get("rwork_size", getattr(value, "rwork_size", value))
            self.iwork_size = kwargs.get("iwork_size", getattr(value, "iwork_size", value))
            self.lwork_size = kwargs.get("lwork_size", getattr(value, "lwork_size", value))
            self.na = kwargs.get("na", getattr(value, "na", value))
            self.nat = kwargs.get("nat", getattr(value, "nat", value))
            self.nm = kwargs.get("nm", getattr(value, "nm", value))
            self.nms = kwargs.get("nms", getattr(value, "nms", value))
            self.nmt = kwargs.get("nmt", getattr(value, "nmt", value))
            self.i_next = kwargs.get("i_next", getattr(value, "i_next", value))
            self.i_step = kwargs.get("i_step", getattr(value, "i_step", value))
            self.i_mult = kwargs.get("i_mult", getattr(value, "i_mult", value))
            self.i_mod = kwargs.get("i_mod", getattr(value, "i_mod", value))
            self.i_iter = kwargs.get("i_iter", getattr(value, "i_iter", value))
            self.smg = kwargs.get("smg", getattr(value, "smg", value))
            self.emg = kwargs.get("emg", getattr(value, "emg", value))
            self.smgm = kwargs.get("smgm", getattr(value, "smgm", value))
            self.emgm = kwargs.get("emgm", getattr(value, "emgm", value))
            self.smgc = kwargs.get("smgc", getattr(value, "smgc", value))
            self.emgc = kwargs.get("emgc", getattr(value, "emgc", value))
            self.sbm = kwargs.get("sbm", getattr(value, "sbm", value))
            self.ebm = kwargs.get("ebm", getattr(value, "ebm", value))
            self.saxb = kwargs.get("saxb", getattr(value, "saxb", value))
            self.eaxb = kwargs.get("eaxb", getattr(value, "eaxb", value))
            self.say = kwargs.get("say", getattr(value, "say", value))
            self.eay = kwargs.get("eay", getattr(value, "eay", value))
            self.smxb = kwargs.get("smxb", getattr(value, "smxb", value))
            self.emxb = kwargs.get("emxb", getattr(value, "emxb", value))
            self.smyb = kwargs.get("smyb", getattr(value, "smyb", value))
            self.emyb = kwargs.get("emyb", getattr(value, "emyb", value))
            self.sag = kwargs.get("sag", getattr(value, "sag", value))
            self.eag = kwargs.get("eag", getattr(value, "eag", value))
            self.saet = kwargs.get("saet", getattr(value, "saet", value))
            self.eaet = kwargs.get("eaet", getattr(value, "eaet", value))
            self.saxs = kwargs.get("saxs", getattr(value, "saxs", value))
            self.eaxs = kwargs.get("eaxs", getattr(value, "eaxs", value))
            self.saxg = kwargs.get("saxg", getattr(value, "saxg", value))
            self.eaxg = kwargs.get("eaxg", getattr(value, "eaxg", value))
            self.sayg = kwargs.get("sayg", getattr(value, "sayg", value))
            self.eayg = kwargs.get("eayg", getattr(value, "eayg", value))
            self.sxg = kwargs.get("sxg", getattr(value, "sxg", value))
            self.exg = kwargs.get("exg", getattr(value, "exg", value))
            self.smet = kwargs.get("smet", getattr(value, "smet", value))
            self.emet = kwargs.get("emet", getattr(value, "emet", value))
            self.smxs = kwargs.get("smxs", getattr(value, "smxs", value))
            self.emxs = kwargs.get("emxs", getattr(value, "emxs", value))
            self.smxg = kwargs.get("smxg", getattr(value, "smxg", value))
            self.emxg = kwargs.get("emxg", getattr(value, "emxg", value))
            self.soet = kwargs.get("soet", getattr(value, "soet", value))
            self.eoet = kwargs.get("eoet", getattr(value, "eoet", value))
            self.seos = kwargs.get("seos", getattr(value, "seos", value))
            self.eeos = kwargs.get("eeos", getattr(value, "eeos", value))
            self.seog = kwargs.get("seog", getattr(value, "seog", value))
            self.eeog = kwargs.get("eeog", getattr(value, "eeog", value))
            self.syg = kwargs.get("syg", getattr(value, "syg", value))
            self.eyg = kwargs.get("eyg", getattr(value, "eyg", value))
            self.saxis = kwargs.get("saxis", getattr(value, "saxis", value))
            self.eaxis = kwargs.get("eaxis", getattr(value, "eaxis", value))
            self.saxir = kwargs.get("saxir", getattr(value, "saxir", value))
            self.eaxir = kwargs.get("eaxir", getattr(value, "eaxir", value))
            self.smxis = kwargs.get("smxis", getattr(value, "smxis", value))
            self.emxis = kwargs.get("emxis", getattr(value, "emxis", value))
            self.smxir = kwargs.get("smxir", getattr(value, "smxir", value))
            self.emxir = kwargs.get("emxir", getattr(value, "emxir", value))
            self.soxis = kwargs.get("soxis", getattr(value, "soxis", value))
            self.eoxis = kwargs.get("eoxis", getattr(value, "eoxis", value))
            self.soxir = kwargs.get("soxir", getattr(value, "soxir", value))
            self.eoxir = kwargs.get("eoxir", getattr(value, "eoxir", value))
            self.sal = kwargs.get("sal", getattr(value, "sal", value))
            self.eal = kwargs.get("eal", getattr(value, "eal", value))
            self.sml = kwargs.get("sml", getattr(value, "sml", value))
            self.eml = kwargs.get("eml", getattr(value, "eml", value))
            self.sast = kwargs.get("sast", getattr(value, "sast", value))
            self.east = kwargs.get("east", getattr(value, "east", value))
            self.smst = kwargs.get("smst", getattr(value, "smst", value))
            self.emst = kwargs.get("emst", getattr(value, "emst", value))
            self.saxi = kwargs.get("saxi", getattr(value, "saxi", value))
            self.eaxi = kwargs.get("eaxi", getattr(value, "eaxi", value))
            self.smxi = kwargs.get("smxi", getattr(value, "smxi", value))
            self.emxi = kwargs.get("emxi", getattr(value, "emxi", value))
            self.soxi = kwargs.get("soxi", getattr(value, "soxi", value))
            self.eoxi = kwargs.get("eoxi", getattr(value, "eoxi", value))
            self.ssb = kwargs.get("ssb", getattr(value, "ssb", value))
            self.esb = kwargs.get("esb", getattr(value, "esb", value))
            self.sao = kwargs.get("sao", getattr(value, "sao", value))
            self.eao = kwargs.get("eao", getattr(value, "eao", value))
            self.smo = kwargs.get("smo", getattr(value, "smo", value))
            self.emo = kwargs.get("emo", getattr(value, "emo", value))
            self.sui = kwargs.get("sui", getattr(value, "sui", value))
            self.eui = kwargs.get("eui", getattr(value, "eui", value))
            self.wint = kwargs.get("wint", getattr(value, "wint", value))
            self.cint = kwargs.get("cint", getattr(value, "cint", value))
            self.wfit = kwargs.get("wfit", getattr(value, "wfit", value))
            self.cfit = kwargs.get("cfit", getattr(value, "cfit", value))
            self.wnrm = kwargs.get("wnrm", getattr(value, "wnrm", value))
            self.cnrm = kwargs.get("cnrm", getattr(value, "cnrm", value))
            self.wgen = kwargs.get("wgen", getattr(value, "wgen", value))
            self.cgen = kwargs.get("cgen", getattr(value, "cgen", value))
            self.wemb = kwargs.get("wemb", getattr(value, "wemb", value))
            self.cemb = kwargs.get("cemb", getattr(value, "cemb", value))
            self.wevl = kwargs.get("wevl", getattr(value, "wevl", value))
            self.cevl = kwargs.get("cevl", getattr(value, "cevl", value))
            self.wgrd = kwargs.get("wgrd", getattr(value, "wgrd", value))
            self.cgrd = kwargs.get("cgrd", getattr(value, "cgrd", value))
            self.wrat = kwargs.get("wrat", getattr(value, "wrat", value))
            self.crat = kwargs.get("crat", getattr(value, "crat", value))
            self.wopt = kwargs.get("wopt", getattr(value, "wopt", value))
            self.copt = kwargs.get("copt", getattr(value, "copt", value))
            self.wcon = kwargs.get("wcon", getattr(value, "wcon", value))
            self.ccon = kwargs.get("ccon", getattr(value, "ccon", value))
            self.wrec = kwargs.get("wrec", getattr(value, "wrec", value))
            self.crec = kwargs.get("crec", getattr(value, "crec", value))
            self.wenc = kwargs.get("wenc", getattr(value, "wenc", value))
            self.cenc = kwargs.get("cenc", getattr(value, "cenc", value))
            self.fit_mse = kwargs.get("fit_mse", getattr(value, "fit_mse", value))
            self.fit_prev_mse = kwargs.get("fit_prev_mse", getattr(value, "fit_prev_mse", value))
            self.fit_best_mse = kwargs.get("fit_best_mse", getattr(value, "fit_best_mse", value))
            self.fit_step_mean_remain = kwargs.get("fit_step_mean_remain", getattr(value, "fit_step_mean_remain", value))
            self.fit_step_curv_remain = kwargs.get("fit_step_curv_remain", getattr(value, "fit_step_curv_remain", value))
            self.fit_total_eval_rank = kwargs.get("fit_total_eval_rank", getattr(value, "fit_total_eval_rank", value))
            self.fit_total_grad_rank = kwargs.get("fit_total_grad_rank", getattr(value, "fit_total_grad_rank", value))
            self.fit_normalize = kwargs.get("fit_normalize", getattr(value, "fit_normalize", value))
            self.fit_step = kwargs.get("fit_step", getattr(value, "fit_step", value))
            self.fit_min_to_update = kwargs.get("fit_min_to_update", getattr(value, "fit_min_to_update", value))
            self.fit_last_interrupt_time = kwargs.get("fit_last_interrupt_time", getattr(value, "fit_last_interrupt_time", value))
            self.fit_wait_time = kwargs.get("fit_wait_time", getattr(value, "fit_wait_time", value))
            self.fit_total_rank = kwargs.get("fit_total_rank", getattr(value, "fit_total_rank", value))
            self.fit_ns = kwargs.get("fit_ns", getattr(value, "fit_ns", value))
            self.fit_nt = kwargs.get("fit_nt", getattr(value, "fit_nt", value))
        # Define a "__str__" that produces a legible summary of this type.
        def __str__(self):
            s = []
            for (n, t) in self._fields_:
                s.append( n + "=" + str(getattr(self,n)) )
            return "MODEL_CONFIG[" + ", ".join(s) + "]"
        # Define an "__eq__" method that checks equality of all fields.
        def __eq__(self, other):
            for (n, t) in self._fields_:
                if (getattr(self, n) != getattr(other, n, None)):
                    return False
            return True
    

    # Declare 'clock_rate'
    def get_clock_rate(self):
        clock_rate = ctypes.c_long()
        clib.axy_get_clock_rate(ctypes.byref(clock_rate))
        return clock_rate.value
    def set_clock_rate(self, clock_rate):
        clock_rate = ctypes.c_long(clock_rate)
        clib.axy_set_clock_rate(ctypes.byref(clock_rate))
    clock_rate = property(get_clock_rate, set_clock_rate)

    # Declare 'clock_max'
    def get_clock_max(self):
        clock_max = ctypes.c_long()
        clib.axy_get_clock_max(ctypes.byref(clock_max))
        return clock_max.value
    def set_clock_max(self, clock_max):
        clock_max = ctypes.c_long(clock_max)
        clib.axy_set_clock_max(ctypes.byref(clock_max))
    clock_max = property(get_clock_max, set_clock_max)

    # Declare 'zero'
    def get_zero(self):
        zero = ctypes.c_long()
        clib.axy_get_zero(ctypes.byref(zero))
        return zero.value
    def set_zero(self, zero):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    zero = property(get_zero, set_zero)

    # Declare 'one'
    def get_one(self):
        one = ctypes.c_long()
        clib.axy_get_one(ctypes.byref(one))
        return one.value
    def set_one(self, one):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    one = property(get_one, set_one)

    # Declare 'two'
    def get_two(self):
        two = ctypes.c_long()
        clib.axy_get_two(ctypes.byref(two))
        return two.value
    def set_two(self, two):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    two = property(get_two, set_two)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine NEW_MODEL_CONFIG
    
    def new_model_config(self, adn, mdn, mdo, noe, ade=None, ane=None, ads=None, ans=None, anc=None, ado=None, mde=None, mne=None, mds=None, mns=None, mnc=None, doe=None, num_threads=None):
        '''! Generate a model configuration given state parameters for the model.
! Size related parameters.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "adn"
        if (type(adn) is not ctypes.c_int): adn = ctypes.c_int(adn)
        
        # Setting up "ade"
        ade_present = ctypes.c_bool(True)
        if (ade is None):
            ade_present = ctypes.c_bool(False)
            ade = ctypes.c_int()
        else:
            ade = ctypes.c_int(ade)
        if (type(ade) is not ctypes.c_int): ade = ctypes.c_int(ade)
        
        # Setting up "ane"
        ane_present = ctypes.c_bool(True)
        if (ane is None):
            ane_present = ctypes.c_bool(False)
            ane = ctypes.c_int()
        else:
            ane = ctypes.c_int(ane)
        if (type(ane) is not ctypes.c_int): ane = ctypes.c_int(ane)
        
        # Setting up "ads"
        ads_present = ctypes.c_bool(True)
        if (ads is None):
            ads_present = ctypes.c_bool(False)
            ads = ctypes.c_int()
        else:
            ads = ctypes.c_int(ads)
        if (type(ads) is not ctypes.c_int): ads = ctypes.c_int(ads)
        
        # Setting up "ans"
        ans_present = ctypes.c_bool(True)
        if (ans is None):
            ans_present = ctypes.c_bool(False)
            ans = ctypes.c_int()
        else:
            ans = ctypes.c_int(ans)
        if (type(ans) is not ctypes.c_int): ans = ctypes.c_int(ans)
        
        # Setting up "anc"
        anc_present = ctypes.c_bool(True)
        if (anc is None):
            anc_present = ctypes.c_bool(False)
            anc = ctypes.c_int()
        else:
            anc = ctypes.c_int(anc)
        if (type(anc) is not ctypes.c_int): anc = ctypes.c_int(anc)
        
        # Setting up "ado"
        ado_present = ctypes.c_bool(True)
        if (ado is None):
            ado_present = ctypes.c_bool(False)
            ado = ctypes.c_int()
        else:
            ado = ctypes.c_int(ado)
        if (type(ado) is not ctypes.c_int): ado = ctypes.c_int(ado)
        
        # Setting up "mdn"
        if (type(mdn) is not ctypes.c_int): mdn = ctypes.c_int(mdn)
        
        # Setting up "mde"
        mde_present = ctypes.c_bool(True)
        if (mde is None):
            mde_present = ctypes.c_bool(False)
            mde = ctypes.c_int()
        else:
            mde = ctypes.c_int(mde)
        if (type(mde) is not ctypes.c_int): mde = ctypes.c_int(mde)
        
        # Setting up "mne"
        mne_present = ctypes.c_bool(True)
        if (mne is None):
            mne_present = ctypes.c_bool(False)
            mne = ctypes.c_int()
        else:
            mne = ctypes.c_int(mne)
        if (type(mne) is not ctypes.c_int): mne = ctypes.c_int(mne)
        
        # Setting up "mds"
        mds_present = ctypes.c_bool(True)
        if (mds is None):
            mds_present = ctypes.c_bool(False)
            mds = ctypes.c_int()
        else:
            mds = ctypes.c_int(mds)
        if (type(mds) is not ctypes.c_int): mds = ctypes.c_int(mds)
        
        # Setting up "mns"
        mns_present = ctypes.c_bool(True)
        if (mns is None):
            mns_present = ctypes.c_bool(False)
            mns = ctypes.c_int()
        else:
            mns = ctypes.c_int(mns)
        if (type(mns) is not ctypes.c_int): mns = ctypes.c_int(mns)
        
        # Setting up "mnc"
        mnc_present = ctypes.c_bool(True)
        if (mnc is None):
            mnc_present = ctypes.c_bool(False)
            mnc = ctypes.c_int()
        else:
            mnc = ctypes.c_int(mnc)
        if (type(mnc) is not ctypes.c_int): mnc = ctypes.c_int(mnc)
        
        # Setting up "mdo"
        if (type(mdo) is not ctypes.c_int): mdo = ctypes.c_int(mdo)
        
        # Setting up "doe"
        doe_present = ctypes.c_bool(True)
        if (doe is None):
            doe_present = ctypes.c_bool(False)
            doe = ctypes.c_int()
        else:
            doe = ctypes.c_int(doe)
        if (type(doe) is not ctypes.c_int): doe = ctypes.c_int(doe)
        
        # Setting up "noe"
        if (type(noe) is not ctypes.c_int): noe = ctypes.c_int(noe)
        
        # Setting up "num_threads"
        num_threads_present = ctypes.c_bool(True)
        if (num_threads is None):
            num_threads_present = ctypes.c_bool(False)
            num_threads = ctypes.c_int()
        else:
            num_threads = ctypes.c_int(num_threads)
        if (type(num_threads) is not ctypes.c_int): num_threads = ctypes.c_int(num_threads)
        
        # Setting up "config"
        config = MODEL_CONFIG()
    
        # Call C-accessible Fortran wrapper.
        clib.c_new_model_config(ctypes.byref(adn), ctypes.byref(ade_present), ctypes.byref(ade), ctypes.byref(ane_present), ctypes.byref(ane), ctypes.byref(ads_present), ctypes.byref(ads), ctypes.byref(ans_present), ctypes.byref(ans), ctypes.byref(anc_present), ctypes.byref(anc), ctypes.byref(ado_present), ctypes.byref(ado), ctypes.byref(mdn), ctypes.byref(mde_present), ctypes.byref(mde), ctypes.byref(mne_present), ctypes.byref(mne), ctypes.byref(mds_present), ctypes.byref(mds), ctypes.byref(mns_present), ctypes.byref(mns), ctypes.byref(mnc_present), ctypes.byref(mnc), ctypes.byref(mdo), ctypes.byref(doe_present), ctypes.byref(doe), ctypes.byref(noe), ctypes.byref(num_threads_present), ctypes.byref(num_threads), ctypes.byref(config))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine NEW_FIT_CONFIG
    
    def new_fit_config(self, nm, config, na=None, nmt=None, nat=None, adi=None, mdi=None, odi=None, seed=None):
        '''! Given a number of X points "NM", and a number of aggregator X points
! "NA", update the "RWORK_SIZE" and "IWORK_SIZE" attributes in "CONFIG"
! as well as all related work indices for that size data. Optionally
! also provide "NAT" and "NMT" the 'total' number of aggregate and
! fixed points respectively.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "nm"
        if (type(nm) is not ctypes.c_long): nm = ctypes.c_long(nm)
        
        # Setting up "na"
        na_present = ctypes.c_bool(True)
        if (na is None):
            na_present = ctypes.c_bool(False)
            na = ctypes.c_long()
        else:
            na = ctypes.c_long(na)
        if (type(na) is not ctypes.c_long): na = ctypes.c_long(na)
        
        # Setting up "nmt"
        nmt_present = ctypes.c_bool(True)
        if (nmt is None):
            nmt_present = ctypes.c_bool(False)
            nmt = ctypes.c_long()
        else:
            nmt = ctypes.c_long(nmt)
        if (type(nmt) is not ctypes.c_long): nmt = ctypes.c_long(nmt)
        
        # Setting up "nat"
        nat_present = ctypes.c_bool(True)
        if (nat is None):
            nat_present = ctypes.c_bool(False)
            nat = ctypes.c_long()
        else:
            nat = ctypes.c_long(nat)
        if (type(nat) is not ctypes.c_long): nat = ctypes.c_long(nat)
        
        # Setting up "adi"
        adi_present = ctypes.c_bool(True)
        if (adi is None):
            adi_present = ctypes.c_bool(False)
            adi = ctypes.c_long()
        else:
            adi = ctypes.c_long(adi)
        if (type(adi) is not ctypes.c_long): adi = ctypes.c_long(adi)
        
        # Setting up "mdi"
        mdi_present = ctypes.c_bool(True)
        if (mdi is None):
            mdi_present = ctypes.c_bool(False)
            mdi = ctypes.c_long()
        else:
            mdi = ctypes.c_long(mdi)
        if (type(mdi) is not ctypes.c_long): mdi = ctypes.c_long(mdi)
        
        # Setting up "odi"
        odi_present = ctypes.c_bool(True)
        if (odi is None):
            odi_present = ctypes.c_bool(False)
            odi = ctypes.c_long()
        else:
            odi = ctypes.c_long(odi)
        if (type(odi) is not ctypes.c_long): odi = ctypes.c_long(odi)
        
        # Setting up "seed"
        seed_present = ctypes.c_bool(True)
        if (seed is None):
            seed_present = ctypes.c_bool(False)
            seed = ctypes.c_long()
        else:
            seed = ctypes.c_long(seed)
        if (type(seed) is not ctypes.c_long): seed = ctypes.c_long(seed)
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
    
        # Call C-accessible Fortran wrapper.
        clib.c_new_fit_config(ctypes.byref(nm), ctypes.byref(na_present), ctypes.byref(na), ctypes.byref(nmt_present), ctypes.byref(nmt), ctypes.byref(nat_present), ctypes.byref(nat), ctypes.byref(adi_present), ctypes.byref(adi), ctypes.byref(mdi_present), ctypes.byref(mdi), ctypes.byref(odi_present), ctypes.byref(odi), ctypes.byref(seed_present), ctypes.byref(seed), ctypes.byref(config))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine INIT_MODEL
    
    def init_model(self, config, model, seed=None, initial_shift_range=None, initial_output_scale=None):
        '''! Initialize the weights for a model, optionally provide a random seed.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "seed"
        seed_present = ctypes.c_bool(True)
        if (seed is None):
            seed_present = ctypes.c_bool(False)
            seed = ctypes.c_long()
        else:
            seed = ctypes.c_long(seed)
        if (type(seed) is not ctypes.c_long): seed = ctypes.c_long(seed)
        
        # Setting up "initial_shift_range"
        initial_shift_range_present = ctypes.c_bool(True)
        if (initial_shift_range is None):
            initial_shift_range_present = ctypes.c_bool(False)
            initial_shift_range = ctypes.c_float()
        else:
            initial_shift_range = ctypes.c_float(initial_shift_range)
        if (type(initial_shift_range) is not ctypes.c_float): initial_shift_range = ctypes.c_float(initial_shift_range)
        
        # Setting up "initial_output_scale"
        initial_output_scale_present = ctypes.c_bool(True)
        if (initial_output_scale is None):
            initial_output_scale_present = ctypes.c_bool(False)
            initial_output_scale = ctypes.c_float()
        else:
            initial_output_scale = ctypes.c_float(initial_output_scale)
        if (type(initial_output_scale) is not ctypes.c_float): initial_output_scale = ctypes.c_float(initial_output_scale)
    
        # Call C-accessible Fortran wrapper.
        clib.c_init_model(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(seed_present), ctypes.byref(seed), ctypes.byref(initial_shift_range_present), ctypes.byref(initial_shift_range), ctypes.byref(initial_output_scale_present), ctypes.byref(initial_output_scale))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, model

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine CHECK_SHAPE
    
    def check_shape(self, config, model, ax, axi, sizes, x, xi, y, yi, for_evaluation=None):
        '''! Return nonzero INFO if any shapes or values do not match expectations.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "axi"
        if ((not issubclass(type(axi), numpy.ndarray)) or
            (not numpy.asarray(axi).flags.f_contiguous) or
            (not (axi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi = numpy.asarray(axi, dtype=ctypes.c_long, order='F')
        axi_dim_1 = ctypes.c_long(axi.shape[0])
        axi_dim_2 = ctypes.c_long(axi.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "xi"
        if ((not issubclass(type(xi), numpy.ndarray)) or
            (not numpy.asarray(xi).flags.f_contiguous) or
            (not (xi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi = numpy.asarray(xi, dtype=ctypes.c_long, order='F')
        xi_dim_1 = ctypes.c_long(xi.shape[0])
        xi_dim_2 = ctypes.c_long(xi.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "yi"
        if ((not issubclass(type(yi), numpy.ndarray)) or
            (not numpy.asarray(yi).flags.f_contiguous) or
            (not (yi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi = numpy.asarray(yi, dtype=ctypes.c_long, order='F')
        yi_dim_1 = ctypes.c_long(yi.shape[0])
        yi_dim_2 = ctypes.c_long(yi.shape[1])
        
        # Setting up "info"
        info = ctypes.c_int()
        
        # Setting up "for_evaluation"
        for_evaluation_present = ctypes.c_bool(True)
        if (for_evaluation is None):
            for_evaluation_present = ctypes.c_bool(False)
            for_evaluation = ctypes.c_bool()
        else:
            for_evaluation = ctypes.c_bool(for_evaluation)
        if (type(for_evaluation) is not ctypes.c_bool): for_evaluation = ctypes.c_bool(for_evaluation)
    
        # Call C-accessible Fortran wrapper.
        clib.c_check_shape(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(axi_dim_1), ctypes.byref(axi_dim_2), ctypes.c_void_p(axi.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(xi_dim_1), ctypes.byref(xi_dim_2), ctypes.c_void_p(xi.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(yi_dim_1), ctypes.byref(yi_dim_2), ctypes.c_void_p(yi.ctypes.data), ctypes.byref(info), ctypes.byref(for_evaluation_present), ctypes.byref(for_evaluation))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine COMPUTE_BATCHES
    
    def compute_batches(self, config, na, nm, sizes, joint, info):
        '''! Given a number of batches, compute the batch start and ends for
!  the aggregator and fixed inputs. Store in (2,_) arrays.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "na"
        if (type(na) is not ctypes.c_long): na = ctypes.c_long(na)
        
        # Setting up "nm"
        if (type(nm) is not ctypes.c_long): nm = ctypes.c_long(nm)
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "batcha_starts"
        batcha_starts = ctypes.c_void_p()
        batcha_starts_dim_1 = ctypes.c_long()
        
        # Setting up "batcha_ends"
        batcha_ends = ctypes.c_void_p()
        batcha_ends_dim_1 = ctypes.c_long()
        
        # Setting up "agg_starts"
        agg_starts = ctypes.c_void_p()
        agg_starts_dim_1 = ctypes.c_long()
        
        # Setting up "fix_starts"
        fix_starts = ctypes.c_void_p()
        fix_starts_dim_1 = ctypes.c_long()
        
        # Setting up "batchm_starts"
        batchm_starts = ctypes.c_void_p()
        batchm_starts_dim_1 = ctypes.c_long()
        
        # Setting up "batchm_ends"
        batchm_ends = ctypes.c_void_p()
        batchm_ends_dim_1 = ctypes.c_long()
        
        # Setting up "joint"
        if (type(joint) is not ctypes.c_bool): joint = ctypes.c_bool(joint)
        
        # Setting up "info"
        if (type(info) is not ctypes.c_int): info = ctypes.c_int(info)
    
        # Call C-accessible Fortran wrapper.
        clib.c_compute_batches(ctypes.byref(config), ctypes.byref(na), ctypes.byref(nm), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(batcha_starts_dim_1), ctypes.byref(batcha_starts), ctypes.byref(batcha_ends_dim_1), ctypes.byref(batcha_ends), ctypes.byref(agg_starts_dim_1), ctypes.byref(agg_starts), ctypes.byref(fix_starts_dim_1), ctypes.byref(fix_starts), ctypes.byref(batchm_starts_dim_1), ctypes.byref(batchm_starts), ctypes.byref(batchm_ends_dim_1), ctypes.byref(batchm_ends), ctypes.byref(joint), ctypes.byref(info))
    
        # Post-processing "batcha_starts"
        batcha_starts_size = (batcha_starts_dim_1.value)
        if (batcha_starts_size > 0):
            batcha_starts = numpy.array(ctypes.cast(batcha_starts, ctypes.POINTER(ctypes.c_long*batcha_starts_size)).contents, copy=False)
        elif (batcha_starts_size == 0):
            batcha_starts = numpy.zeros(shape=(batcha_starts_dim_1.value), dtype=ctypes.c_long, order='F')
        else:
            batcha_starts = None
        
        # Post-processing "batcha_ends"
        batcha_ends_size = (batcha_ends_dim_1.value)
        if (batcha_ends_size > 0):
            batcha_ends = numpy.array(ctypes.cast(batcha_ends, ctypes.POINTER(ctypes.c_long*batcha_ends_size)).contents, copy=False)
        elif (batcha_ends_size == 0):
            batcha_ends = numpy.zeros(shape=(batcha_ends_dim_1.value), dtype=ctypes.c_long, order='F')
        else:
            batcha_ends = None
        
        # Post-processing "agg_starts"
        agg_starts_size = (agg_starts_dim_1.value)
        if (agg_starts_size > 0):
            agg_starts = numpy.array(ctypes.cast(agg_starts, ctypes.POINTER(ctypes.c_long*agg_starts_size)).contents, copy=False)
        elif (agg_starts_size == 0):
            agg_starts = numpy.zeros(shape=(agg_starts_dim_1.value), dtype=ctypes.c_long, order='F')
        else:
            agg_starts = None
        
        # Post-processing "fix_starts"
        fix_starts_size = (fix_starts_dim_1.value)
        if (fix_starts_size > 0):
            fix_starts = numpy.array(ctypes.cast(fix_starts, ctypes.POINTER(ctypes.c_long*fix_starts_size)).contents, copy=False)
        elif (fix_starts_size == 0):
            fix_starts = numpy.zeros(shape=(fix_starts_dim_1.value), dtype=ctypes.c_long, order='F')
        else:
            fix_starts = None
        
        # Post-processing "batchm_starts"
        batchm_starts_size = (batchm_starts_dim_1.value)
        if (batchm_starts_size > 0):
            batchm_starts = numpy.array(ctypes.cast(batchm_starts, ctypes.POINTER(ctypes.c_long*batchm_starts_size)).contents, copy=False)
        elif (batchm_starts_size == 0):
            batchm_starts = numpy.zeros(shape=(batchm_starts_dim_1.value), dtype=ctypes.c_long, order='F')
        else:
            batchm_starts = None
        
        # Post-processing "batchm_ends"
        batchm_ends_size = (batchm_ends_dim_1.value)
        if (batchm_ends_size > 0):
            batchm_ends = numpy.array(ctypes.cast(batchm_ends, ctypes.POINTER(ctypes.c_long*batchm_ends_size)).contents, copy=False)
        elif (batchm_ends_size == 0):
            batchm_ends = numpy.zeros(shape=(batchm_ends_dim_1.value), dtype=ctypes.c_long, order='F')
        else:
            batchm_ends = None
        
        # Return final results, 'INTENT(OUT)' arguments only.
        return batcha_starts, batcha_ends, agg_starts, fix_starts, batchm_starts, batchm_ends, info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine FETCH_DATA
    
    def fetch_data(self, config, agg_iterators_in, ax_in, ax, axi_in, axi, sizes_in, sizes, x_in, x, xi_in, xi, y_in, y, yi_in, yi, yw_in, yw):
        '''! Give the raw input data, fetch a new set of data that fits in memory.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "agg_iterators_in"
        if ((not issubclass(type(agg_iterators_in), numpy.ndarray)) or
            (not numpy.asarray(agg_iterators_in).flags.f_contiguous) or
            (not (agg_iterators_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'agg_iterators_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            agg_iterators_in = numpy.asarray(agg_iterators_in, dtype=ctypes.c_long, order='F')
        agg_iterators_in_dim_1 = ctypes.c_long(agg_iterators_in.shape[0])
        agg_iterators_in_dim_2 = ctypes.c_long(agg_iterators_in.shape[1])
        
        # Setting up "ax_in"
        if ((not issubclass(type(ax_in), numpy.ndarray)) or
            (not numpy.asarray(ax_in).flags.f_contiguous) or
            (not (ax_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax_in = numpy.asarray(ax_in, dtype=ctypes.c_float, order='F')
        ax_in_dim_1 = ctypes.c_long(ax_in.shape[0])
        ax_in_dim_2 = ctypes.c_long(ax_in.shape[1])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "axi_in"
        if ((not issubclass(type(axi_in), numpy.ndarray)) or
            (not numpy.asarray(axi_in).flags.f_contiguous) or
            (not (axi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi_in = numpy.asarray(axi_in, dtype=ctypes.c_long, order='F')
        axi_in_dim_1 = ctypes.c_long(axi_in.shape[0])
        axi_in_dim_2 = ctypes.c_long(axi_in.shape[1])
        
        # Setting up "axi"
        if ((not issubclass(type(axi), numpy.ndarray)) or
            (not numpy.asarray(axi).flags.f_contiguous) or
            (not (axi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi = numpy.asarray(axi, dtype=ctypes.c_long, order='F')
        axi_dim_1 = ctypes.c_long(axi.shape[0])
        axi_dim_2 = ctypes.c_long(axi.shape[1])
        
        # Setting up "sizes_in"
        if ((not issubclass(type(sizes_in), numpy.ndarray)) or
            (not numpy.asarray(sizes_in).flags.f_contiguous) or
            (not (sizes_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes_in = numpy.asarray(sizes_in, dtype=ctypes.c_long, order='F')
        sizes_in_dim_1 = ctypes.c_long(sizes_in.shape[0])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x_in"
        if ((not issubclass(type(x_in), numpy.ndarray)) or
            (not numpy.asarray(x_in).flags.f_contiguous) or
            (not (x_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x_in = numpy.asarray(x_in, dtype=ctypes.c_float, order='F')
        x_in_dim_1 = ctypes.c_long(x_in.shape[0])
        x_in_dim_2 = ctypes.c_long(x_in.shape[1])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "xi_in"
        if ((not issubclass(type(xi_in), numpy.ndarray)) or
            (not numpy.asarray(xi_in).flags.f_contiguous) or
            (not (xi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi_in = numpy.asarray(xi_in, dtype=ctypes.c_long, order='F')
        xi_in_dim_1 = ctypes.c_long(xi_in.shape[0])
        xi_in_dim_2 = ctypes.c_long(xi_in.shape[1])
        
        # Setting up "xi"
        if ((not issubclass(type(xi), numpy.ndarray)) or
            (not numpy.asarray(xi).flags.f_contiguous) or
            (not (xi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi = numpy.asarray(xi, dtype=ctypes.c_long, order='F')
        xi_dim_1 = ctypes.c_long(xi.shape[0])
        xi_dim_2 = ctypes.c_long(xi.shape[1])
        
        # Setting up "y_in"
        if ((not issubclass(type(y_in), numpy.ndarray)) or
            (not numpy.asarray(y_in).flags.f_contiguous) or
            (not (y_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_in = numpy.asarray(y_in, dtype=ctypes.c_float, order='F')
        y_in_dim_1 = ctypes.c_long(y_in.shape[0])
        y_in_dim_2 = ctypes.c_long(y_in.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "yi_in"
        if ((not issubclass(type(yi_in), numpy.ndarray)) or
            (not numpy.asarray(yi_in).flags.f_contiguous) or
            (not (yi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi_in = numpy.asarray(yi_in, dtype=ctypes.c_long, order='F')
        yi_in_dim_1 = ctypes.c_long(yi_in.shape[0])
        yi_in_dim_2 = ctypes.c_long(yi_in.shape[1])
        
        # Setting up "yi"
        if ((not issubclass(type(yi), numpy.ndarray)) or
            (not numpy.asarray(yi).flags.f_contiguous) or
            (not (yi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi = numpy.asarray(yi, dtype=ctypes.c_long, order='F')
        yi_dim_1 = ctypes.c_long(yi.shape[0])
        yi_dim_2 = ctypes.c_long(yi.shape[1])
        
        # Setting up "yw_in"
        if ((not issubclass(type(yw_in), numpy.ndarray)) or
            (not numpy.asarray(yw_in).flags.f_contiguous) or
            (not (yw_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw_in = numpy.asarray(yw_in, dtype=ctypes.c_float, order='F')
        yw_in_dim_1 = ctypes.c_long(yw_in.shape[0])
        yw_in_dim_2 = ctypes.c_long(yw_in.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
        
        # Setting up "na"
        na = ctypes.c_long()
        
        # Setting up "nm"
        nm = ctypes.c_long()
    
        # Call C-accessible Fortran wrapper.
        clib.c_fetch_data(ctypes.byref(config), ctypes.byref(agg_iterators_in_dim_1), ctypes.byref(agg_iterators_in_dim_2), ctypes.c_void_p(agg_iterators_in.ctypes.data), ctypes.byref(ax_in_dim_1), ctypes.byref(ax_in_dim_2), ctypes.c_void_p(ax_in.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(axi_in_dim_1), ctypes.byref(axi_in_dim_2), ctypes.c_void_p(axi_in.ctypes.data), ctypes.byref(axi_dim_1), ctypes.byref(axi_dim_2), ctypes.c_void_p(axi.ctypes.data), ctypes.byref(sizes_in_dim_1), ctypes.c_void_p(sizes_in.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_in_dim_1), ctypes.byref(x_in_dim_2), ctypes.c_void_p(x_in.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(xi_in_dim_1), ctypes.byref(xi_in_dim_2), ctypes.c_void_p(xi_in.ctypes.data), ctypes.byref(xi_dim_1), ctypes.byref(xi_dim_2), ctypes.c_void_p(xi.ctypes.data), ctypes.byref(y_in_dim_1), ctypes.byref(y_in_dim_2), ctypes.c_void_p(y_in.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(yi_in_dim_1), ctypes.byref(yi_in_dim_2), ctypes.c_void_p(yi_in.ctypes.data), ctypes.byref(yi_dim_1), ctypes.byref(yi_dim_2), ctypes.c_void_p(yi.ctypes.data), ctypes.byref(yw_in_dim_1), ctypes.byref(yw_in_dim_2), ctypes.c_void_p(yw_in.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data), ctypes.byref(na), ctypes.byref(nm))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, agg_iterators_in, ax, axi, sizes, x, xi, y, yi, yw, na.value, nm.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine EMBED
    
    def embed(self, config, model, axi, xi, ax, x):
        '''! Given a model and mixed real and integer inputs, embed the integer
!  inputs into their appropriate real-value-only formats.
!
! TODO: Should this routine check for usage errors since it is expected
!       to be called by external users when evaluating a model?'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "axi"
        if ((not issubclass(type(axi), numpy.ndarray)) or
            (not numpy.asarray(axi).flags.f_contiguous) or
            (not (axi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi = numpy.asarray(axi, dtype=ctypes.c_long, order='F')
        axi_dim_1 = ctypes.c_long(axi.shape[0])
        axi_dim_2 = ctypes.c_long(axi.shape[1])
        
        # Setting up "xi"
        if ((not issubclass(type(xi), numpy.ndarray)) or
            (not numpy.asarray(xi).flags.f_contiguous) or
            (not (xi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi = numpy.asarray(xi, dtype=ctypes.c_long, order='F')
        xi_dim_1 = ctypes.c_long(xi.shape[0])
        xi_dim_2 = ctypes.c_long(xi.shape[1])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
    
        # Call C-accessible Fortran wrapper.
        clib.c_embed(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(axi_dim_1), ctypes.byref(axi_dim_2), ctypes.c_void_p(axi.ctypes.data), ctypes.byref(xi_dim_1), ctypes.byref(xi_dim_2), ctypes.c_void_p(xi.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, ax, x

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine NORMALIZE_INPUTS
    
    def normalize_inputs(self, config, model, ax, sizes, x):
        '''! Normalize numeric input values (for prediction time).'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "info"
        info = ctypes.c_int()
    
        # Call C-accessible Fortran wrapper.
        clib.c_normalize_inputs(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(info))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return ax, x, info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine EVALUATE
    
    def evaluate(self, config, model, ax, ay, sizes, x, y, a_states, m_states, info):
        '''! Evaluate the piecewise linear regression model, assume already-embedded inputs.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "ay"
        if ((not issubclass(type(ay), numpy.ndarray)) or
            (not numpy.asarray(ay).flags.f_contiguous) or
            (not (ay.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay = numpy.asarray(ay, dtype=ctypes.c_float, order='F')
        ay_dim_1 = ctypes.c_long(ay.shape[0])
        ay_dim_2 = ctypes.c_long(ay.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "a_states"
        if ((not issubclass(type(a_states), numpy.ndarray)) or
            (not numpy.asarray(a_states).flags.f_contiguous) or
            (not (a_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_states = numpy.asarray(a_states, dtype=ctypes.c_float, order='F')
        a_states_dim_1 = ctypes.c_long(a_states.shape[0])
        a_states_dim_2 = ctypes.c_long(a_states.shape[1])
        a_states_dim_3 = ctypes.c_long(a_states.shape[2])
        
        # Setting up "m_states"
        if ((not issubclass(type(m_states), numpy.ndarray)) or
            (not numpy.asarray(m_states).flags.f_contiguous) or
            (not (m_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_states = numpy.asarray(m_states, dtype=ctypes.c_float, order='F')
        m_states_dim_1 = ctypes.c_long(m_states.shape[0])
        m_states_dim_2 = ctypes.c_long(m_states.shape[1])
        m_states_dim_3 = ctypes.c_long(m_states.shape[2])
        
        # Setting up "info"
        if (type(info) is not ctypes.c_int): info = ctypes.c_int(info)
    
        # Call C-accessible Fortran wrapper.
        clib.c_evaluate(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(ay_dim_1), ctypes.byref(ay_dim_2), ctypes.c_void_p(ay.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(a_states_dim_1), ctypes.byref(a_states_dim_2), ctypes.byref(a_states_dim_3), ctypes.c_void_p(a_states.ctypes.data), ctypes.byref(m_states_dim_1), ctypes.byref(m_states_dim_2), ctypes.byref(m_states_dim_3), ctypes.c_void_p(m_states.ctypes.data), ctypes.byref(info))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, ax, ay, x, y, a_states, m_states, info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine EMBEDDING_GRADIENT
    
    def embedding_gradient(self, mde, mne, pairwise, int_inputs, grad, embedding_grad, temp_grad):
        '''! Compute the gradient with respect to embeddings given the input
!  gradient by aggregating over the repeated occurrences of the embedding.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "mde"
        if (type(mde) is not ctypes.c_int): mde = ctypes.c_int(mde)
        
        # Setting up "mne"
        if (type(mne) is not ctypes.c_int): mne = ctypes.c_int(mne)
        
        # Setting up "pairwise"
        if (type(pairwise) is not ctypes.c_bool): pairwise = ctypes.c_bool(pairwise)
        
        # Setting up "int_inputs"
        if ((not issubclass(type(int_inputs), numpy.ndarray)) or
            (not numpy.asarray(int_inputs).flags.f_contiguous) or
            (not (int_inputs.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'int_inputs' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            int_inputs = numpy.asarray(int_inputs, dtype=ctypes.c_long, order='F')
        int_inputs_dim_1 = ctypes.c_long(int_inputs.shape[0])
        int_inputs_dim_2 = ctypes.c_long(int_inputs.shape[1])
        
        # Setting up "grad"
        if ((not issubclass(type(grad), numpy.ndarray)) or
            (not numpy.asarray(grad).flags.f_contiguous) or
            (not (grad.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'grad' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            grad = numpy.asarray(grad, dtype=ctypes.c_float, order='F')
        grad_dim_1 = ctypes.c_long(grad.shape[0])
        grad_dim_2 = ctypes.c_long(grad.shape[1])
        
        # Setting up "embedding_grad"
        if ((not issubclass(type(embedding_grad), numpy.ndarray)) or
            (not numpy.asarray(embedding_grad).flags.f_contiguous) or
            (not (embedding_grad.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'embedding_grad' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            embedding_grad = numpy.asarray(embedding_grad, dtype=ctypes.c_float, order='F')
        embedding_grad_dim_1 = ctypes.c_long(embedding_grad.shape[0])
        embedding_grad_dim_2 = ctypes.c_long(embedding_grad.shape[1])
        
        # Setting up "temp_grad"
        if ((not issubclass(type(temp_grad), numpy.ndarray)) or
            (not numpy.asarray(temp_grad).flags.f_contiguous) or
            (not (temp_grad.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'temp_grad' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            temp_grad = numpy.asarray(temp_grad, dtype=ctypes.c_float, order='F')
        temp_grad_dim_1 = ctypes.c_long(temp_grad.shape[0])
        temp_grad_dim_2 = ctypes.c_long(temp_grad.shape[1])
    
        # Call C-accessible Fortran wrapper.
        clib.c_embedding_gradient(ctypes.byref(mde), ctypes.byref(mne), ctypes.byref(pairwise), ctypes.byref(int_inputs_dim_1), ctypes.byref(int_inputs_dim_2), ctypes.c_void_p(int_inputs.ctypes.data), ctypes.byref(grad_dim_1), ctypes.byref(grad_dim_2), ctypes.c_void_p(grad.ctypes.data), ctypes.byref(embedding_grad_dim_1), ctypes.byref(embedding_grad_dim_2), ctypes.c_void_p(embedding_grad.ctypes.data), ctypes.byref(temp_grad_dim_1), ctypes.byref(temp_grad_dim_2), ctypes.c_void_p(temp_grad.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return embedding_grad, temp_grad

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine BASIS_GRADIENT
    
    def basis_gradient(self, config, model, y, x, ax, sizes, m_states, a_states, ay, grad, batcha_starts, batcha_ends, agg_starts, fix_starts, batchm_starts, batchm_ends, nt):
        '''! Given the values at all internal states in the model and an output
!  gradient, propogate the output gradient through the model and
!  return the gradient of all basis functions.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "m_states"
        if ((not issubclass(type(m_states), numpy.ndarray)) or
            (not numpy.asarray(m_states).flags.f_contiguous) or
            (not (m_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_states = numpy.asarray(m_states, dtype=ctypes.c_float, order='F')
        m_states_dim_1 = ctypes.c_long(m_states.shape[0])
        m_states_dim_2 = ctypes.c_long(m_states.shape[1])
        m_states_dim_3 = ctypes.c_long(m_states.shape[2])
        
        # Setting up "a_states"
        if ((not issubclass(type(a_states), numpy.ndarray)) or
            (not numpy.asarray(a_states).flags.f_contiguous) or
            (not (a_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_states = numpy.asarray(a_states, dtype=ctypes.c_float, order='F')
        a_states_dim_1 = ctypes.c_long(a_states.shape[0])
        a_states_dim_2 = ctypes.c_long(a_states.shape[1])
        a_states_dim_3 = ctypes.c_long(a_states.shape[2])
        
        # Setting up "ay"
        if ((not issubclass(type(ay), numpy.ndarray)) or
            (not numpy.asarray(ay).flags.f_contiguous) or
            (not (ay.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay = numpy.asarray(ay, dtype=ctypes.c_float, order='F')
        ay_dim_1 = ctypes.c_long(ay.shape[0])
        ay_dim_2 = ctypes.c_long(ay.shape[1])
        
        # Setting up "grad"
        if ((not issubclass(type(grad), numpy.ndarray)) or
            (not numpy.asarray(grad).flags.f_contiguous) or
            (not (grad.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'grad' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            grad = numpy.asarray(grad, dtype=ctypes.c_float, order='F')
        grad_dim_1 = ctypes.c_long(grad.shape[0])
        grad_dim_2 = ctypes.c_long(grad.shape[1])
        
        # Setting up "batcha_starts"
        if ((not issubclass(type(batcha_starts), numpy.ndarray)) or
            (not numpy.asarray(batcha_starts).flags.f_contiguous) or
            (not (batcha_starts.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'batcha_starts' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            batcha_starts = numpy.asarray(batcha_starts, dtype=ctypes.c_long, order='F')
        batcha_starts_dim_1 = ctypes.c_long(batcha_starts.shape[0])
        
        # Setting up "batcha_ends"
        if ((not issubclass(type(batcha_ends), numpy.ndarray)) or
            (not numpy.asarray(batcha_ends).flags.f_contiguous) or
            (not (batcha_ends.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'batcha_ends' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            batcha_ends = numpy.asarray(batcha_ends, dtype=ctypes.c_long, order='F')
        batcha_ends_dim_1 = ctypes.c_long(batcha_ends.shape[0])
        
        # Setting up "agg_starts"
        if ((not issubclass(type(agg_starts), numpy.ndarray)) or
            (not numpy.asarray(agg_starts).flags.f_contiguous) or
            (not (agg_starts.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'agg_starts' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            agg_starts = numpy.asarray(agg_starts, dtype=ctypes.c_long, order='F')
        agg_starts_dim_1 = ctypes.c_long(agg_starts.shape[0])
        
        # Setting up "fix_starts"
        if ((not issubclass(type(fix_starts), numpy.ndarray)) or
            (not numpy.asarray(fix_starts).flags.f_contiguous) or
            (not (fix_starts.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'fix_starts' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            fix_starts = numpy.asarray(fix_starts, dtype=ctypes.c_long, order='F')
        fix_starts_dim_1 = ctypes.c_long(fix_starts.shape[0])
        
        # Setting up "batchm_starts"
        if ((not issubclass(type(batchm_starts), numpy.ndarray)) or
            (not numpy.asarray(batchm_starts).flags.f_contiguous) or
            (not (batchm_starts.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'batchm_starts' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            batchm_starts = numpy.asarray(batchm_starts, dtype=ctypes.c_long, order='F')
        batchm_starts_dim_1 = ctypes.c_long(batchm_starts.shape[0])
        
        # Setting up "batchm_ends"
        if ((not issubclass(type(batchm_ends), numpy.ndarray)) or
            (not numpy.asarray(batchm_ends).flags.f_contiguous) or
            (not (batchm_ends.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'batchm_ends' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            batchm_ends = numpy.asarray(batchm_ends, dtype=ctypes.c_long, order='F')
        batchm_ends_dim_1 = ctypes.c_long(batchm_ends.shape[0])
        
        # Setting up "nt"
        if (type(nt) is not ctypes.c_long): nt = ctypes.c_long(nt)
    
        # Call C-accessible Fortran wrapper.
        clib.c_basis_gradient(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(m_states_dim_1), ctypes.byref(m_states_dim_2), ctypes.byref(m_states_dim_3), ctypes.c_void_p(m_states.ctypes.data), ctypes.byref(a_states_dim_1), ctypes.byref(a_states_dim_2), ctypes.byref(a_states_dim_3), ctypes.c_void_p(a_states.ctypes.data), ctypes.byref(ay_dim_1), ctypes.byref(ay_dim_2), ctypes.c_void_p(ay.ctypes.data), ctypes.byref(grad_dim_1), ctypes.byref(grad_dim_2), ctypes.c_void_p(grad.ctypes.data), ctypes.byref(batcha_starts_dim_1), ctypes.c_void_p(batcha_starts.ctypes.data), ctypes.byref(batcha_ends_dim_1), ctypes.c_void_p(batcha_ends.ctypes.data), ctypes.byref(agg_starts_dim_1), ctypes.c_void_p(agg_starts.ctypes.data), ctypes.byref(fix_starts_dim_1), ctypes.c_void_p(fix_starts.ctypes.data), ctypes.byref(batchm_starts_dim_1), ctypes.c_void_p(batchm_starts.ctypes.data), ctypes.byref(batchm_ends_dim_1), ctypes.c_void_p(batchm_ends.ctypes.data), ctypes.byref(nt))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return x, ax, m_states, a_states, ay, grad

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine OUTPUT_GRADIENT
    
    def output_gradient(self, config, y_gradient, y, yi, yw, o_emb_vecs, emb_outs, emb_grads, ssg, don, o_emb_grad=None):
        '''! Given the model output values "Y_GRADIENT", the 'true' numeric
! values "Y", and the true categorical values "YI", produce the
! gradient at the output and store it in "Y_GRADIENT".'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "y_gradient"
        if ((not issubclass(type(y_gradient), numpy.ndarray)) or
            (not numpy.asarray(y_gradient).flags.f_contiguous) or
            (not (y_gradient.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_gradient' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_gradient = numpy.asarray(y_gradient, dtype=ctypes.c_float, order='F')
        y_gradient_dim_1 = ctypes.c_long(y_gradient.shape[0])
        y_gradient_dim_2 = ctypes.c_long(y_gradient.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "yi"
        if ((not issubclass(type(yi), numpy.ndarray)) or
            (not numpy.asarray(yi).flags.f_contiguous) or
            (not (yi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi = numpy.asarray(yi, dtype=ctypes.c_long, order='F')
        yi_dim_1 = ctypes.c_long(yi.shape[0])
        yi_dim_2 = ctypes.c_long(yi.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
        
        # Setting up "o_emb_vecs"
        if ((not issubclass(type(o_emb_vecs), numpy.ndarray)) or
            (not numpy.asarray(o_emb_vecs).flags.f_contiguous) or
            (not (o_emb_vecs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'o_emb_vecs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            o_emb_vecs = numpy.asarray(o_emb_vecs, dtype=ctypes.c_float, order='F')
        o_emb_vecs_dim_1 = ctypes.c_long(o_emb_vecs.shape[0])
        o_emb_vecs_dim_2 = ctypes.c_long(o_emb_vecs.shape[1])
        
        # Setting up "o_emb_grad"
        if (o_emb_grad is None):
            o_emb_grad = numpy.zeros(shape=(config%doe, config%noe), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(o_emb_grad), numpy.ndarray)) or
              (not numpy.asarray(o_emb_grad).flags.f_contiguous) or
              (not (o_emb_grad.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'o_emb_grad' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            o_emb_grad = numpy.asarray(o_emb_grad, dtype=ctypes.c_float, order='F')
        o_emb_grad_dim_1 = ctypes.c_long(o_emb_grad.shape[0])
        o_emb_grad_dim_2 = ctypes.c_long(o_emb_grad.shape[1])
        
        # Setting up "emb_outs"
        if ((not issubclass(type(emb_outs), numpy.ndarray)) or
            (not numpy.asarray(emb_outs).flags.f_contiguous) or
            (not (emb_outs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'emb_outs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            emb_outs = numpy.asarray(emb_outs, dtype=ctypes.c_float, order='F')
        emb_outs_dim_1 = ctypes.c_long(emb_outs.shape[0])
        emb_outs_dim_2 = ctypes.c_long(emb_outs.shape[1])
        
        # Setting up "emb_grads"
        if ((not issubclass(type(emb_grads), numpy.ndarray)) or
            (not numpy.asarray(emb_grads).flags.f_contiguous) or
            (not (emb_grads.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'emb_grads' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            emb_grads = numpy.asarray(emb_grads, dtype=ctypes.c_float, order='F')
        emb_grads_dim_1 = ctypes.c_long(emb_grads.shape[0])
        emb_grads_dim_2 = ctypes.c_long(emb_grads.shape[1])
        
        # Setting up "ssg"
        if (type(ssg) is not ctypes.c_float): ssg = ctypes.c_float(ssg)
        
        # Setting up "don"
        if (type(don) is not ctypes.c_int): don = ctypes.c_int(don)
    
        # Call C-accessible Fortran wrapper.
        clib.c_output_gradient(ctypes.byref(config), ctypes.byref(y_gradient_dim_1), ctypes.byref(y_gradient_dim_2), ctypes.c_void_p(y_gradient.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(yi_dim_1), ctypes.byref(yi_dim_2), ctypes.c_void_p(yi.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data), ctypes.byref(o_emb_vecs_dim_1), ctypes.byref(o_emb_vecs_dim_2), ctypes.c_void_p(o_emb_vecs.ctypes.data), ctypes.byref(o_emb_grad_dim_1), ctypes.byref(o_emb_grad_dim_2), ctypes.c_void_p(o_emb_grad.ctypes.data), ctypes.byref(emb_outs_dim_1), ctypes.byref(emb_outs_dim_2), ctypes.c_void_p(emb_outs.ctypes.data), ctypes.byref(emb_grads_dim_1), ctypes.byref(emb_grads_dim_2), ctypes.c_void_p(emb_grads.ctypes.data), ctypes.byref(ssg), ctypes.byref(don))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, y_gradient, o_emb_grad, emb_outs, emb_grads, ssg.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine MODEL_GRADIENT
    
    def model_gradient(self, config, model, ax, axi, sizes, x, xi, y, yi, yw, sum_squared_gradient, model_grad, info, ay_gradient, y_gradient, a_grads, m_grads, a_emb_temp, m_emb_temp, emb_outs, emb_grads):
        '''! Compute the gradient of the sum of squared error of this regression
! model with respect to its variables given input and output pairs.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "axi"
        if ((not issubclass(type(axi), numpy.ndarray)) or
            (not numpy.asarray(axi).flags.f_contiguous) or
            (not (axi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi = numpy.asarray(axi, dtype=ctypes.c_long, order='F')
        axi_dim_1 = ctypes.c_long(axi.shape[0])
        axi_dim_2 = ctypes.c_long(axi.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "xi"
        if ((not issubclass(type(xi), numpy.ndarray)) or
            (not numpy.asarray(xi).flags.f_contiguous) or
            (not (xi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi = numpy.asarray(xi, dtype=ctypes.c_long, order='F')
        xi_dim_1 = ctypes.c_long(xi.shape[0])
        xi_dim_2 = ctypes.c_long(xi.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "yi"
        if ((not issubclass(type(yi), numpy.ndarray)) or
            (not numpy.asarray(yi).flags.f_contiguous) or
            (not (yi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi = numpy.asarray(yi, dtype=ctypes.c_long, order='F')
        yi_dim_1 = ctypes.c_long(yi.shape[0])
        yi_dim_2 = ctypes.c_long(yi.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
        
        # Setting up "sum_squared_gradient"
        if (type(sum_squared_gradient) is not ctypes.c_float): sum_squared_gradient = ctypes.c_float(sum_squared_gradient)
        
        # Setting up "model_grad"
        if ((not issubclass(type(model_grad), numpy.ndarray)) or
            (not numpy.asarray(model_grad).flags.f_contiguous) or
            (not (model_grad.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model_grad' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model_grad = numpy.asarray(model_grad, dtype=ctypes.c_float, order='F')
        model_grad_dim_1 = ctypes.c_long(model_grad.shape[0])
        model_grad_dim_2 = ctypes.c_long(model_grad.shape[1])
        
        # Setting up "info"
        if (type(info) is not ctypes.c_int): info = ctypes.c_int(info)
        
        # Setting up "ay_gradient"
        if ((not issubclass(type(ay_gradient), numpy.ndarray)) or
            (not numpy.asarray(ay_gradient).flags.f_contiguous) or
            (not (ay_gradient.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay_gradient' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay_gradient = numpy.asarray(ay_gradient, dtype=ctypes.c_float, order='F')
        ay_gradient_dim_1 = ctypes.c_long(ay_gradient.shape[0])
        ay_gradient_dim_2 = ctypes.c_long(ay_gradient.shape[1])
        
        # Setting up "y_gradient"
        if ((not issubclass(type(y_gradient), numpy.ndarray)) or
            (not numpy.asarray(y_gradient).flags.f_contiguous) or
            (not (y_gradient.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_gradient' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_gradient = numpy.asarray(y_gradient, dtype=ctypes.c_float, order='F')
        y_gradient_dim_1 = ctypes.c_long(y_gradient.shape[0])
        y_gradient_dim_2 = ctypes.c_long(y_gradient.shape[1])
        
        # Setting up "a_grads"
        if ((not issubclass(type(a_grads), numpy.ndarray)) or
            (not numpy.asarray(a_grads).flags.f_contiguous) or
            (not (a_grads.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_grads' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_grads = numpy.asarray(a_grads, dtype=ctypes.c_float, order='F')
        a_grads_dim_1 = ctypes.c_long(a_grads.shape[0])
        a_grads_dim_2 = ctypes.c_long(a_grads.shape[1])
        a_grads_dim_3 = ctypes.c_long(a_grads.shape[2])
        
        # Setting up "m_grads"
        if ((not issubclass(type(m_grads), numpy.ndarray)) or
            (not numpy.asarray(m_grads).flags.f_contiguous) or
            (not (m_grads.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_grads' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_grads = numpy.asarray(m_grads, dtype=ctypes.c_float, order='F')
        m_grads_dim_1 = ctypes.c_long(m_grads.shape[0])
        m_grads_dim_2 = ctypes.c_long(m_grads.shape[1])
        m_grads_dim_3 = ctypes.c_long(m_grads.shape[2])
        
        # Setting up "a_emb_temp"
        if ((not issubclass(type(a_emb_temp), numpy.ndarray)) or
            (not numpy.asarray(a_emb_temp).flags.f_contiguous) or
            (not (a_emb_temp.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_emb_temp' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_emb_temp = numpy.asarray(a_emb_temp, dtype=ctypes.c_float, order='F')
        a_emb_temp_dim_1 = ctypes.c_long(a_emb_temp.shape[0])
        a_emb_temp_dim_2 = ctypes.c_long(a_emb_temp.shape[1])
        a_emb_temp_dim_3 = ctypes.c_long(a_emb_temp.shape[2])
        
        # Setting up "m_emb_temp"
        if ((not issubclass(type(m_emb_temp), numpy.ndarray)) or
            (not numpy.asarray(m_emb_temp).flags.f_contiguous) or
            (not (m_emb_temp.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_emb_temp' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_emb_temp = numpy.asarray(m_emb_temp, dtype=ctypes.c_float, order='F')
        m_emb_temp_dim_1 = ctypes.c_long(m_emb_temp.shape[0])
        m_emb_temp_dim_2 = ctypes.c_long(m_emb_temp.shape[1])
        m_emb_temp_dim_3 = ctypes.c_long(m_emb_temp.shape[2])
        
        # Setting up "emb_outs"
        if ((not issubclass(type(emb_outs), numpy.ndarray)) or
            (not numpy.asarray(emb_outs).flags.f_contiguous) or
            (not (emb_outs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'emb_outs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            emb_outs = numpy.asarray(emb_outs, dtype=ctypes.c_float, order='F')
        emb_outs_dim_1 = ctypes.c_long(emb_outs.shape[0])
        emb_outs_dim_2 = ctypes.c_long(emb_outs.shape[1])
        
        # Setting up "emb_grads"
        if ((not issubclass(type(emb_grads), numpy.ndarray)) or
            (not numpy.asarray(emb_grads).flags.f_contiguous) or
            (not (emb_grads.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'emb_grads' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            emb_grads = numpy.asarray(emb_grads, dtype=ctypes.c_float, order='F')
        emb_grads_dim_1 = ctypes.c_long(emb_grads.shape[0])
        emb_grads_dim_2 = ctypes.c_long(emb_grads.shape[1])
    
        # Call C-accessible Fortran wrapper.
        clib.c_model_gradient(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(axi_dim_1), ctypes.byref(axi_dim_2), ctypes.c_void_p(axi.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(xi_dim_1), ctypes.byref(xi_dim_2), ctypes.c_void_p(xi.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(yi_dim_1), ctypes.byref(yi_dim_2), ctypes.c_void_p(yi.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data), ctypes.byref(sum_squared_gradient), ctypes.byref(model_grad_dim_1), ctypes.byref(model_grad_dim_2), ctypes.c_void_p(model_grad.ctypes.data), ctypes.byref(info), ctypes.byref(ay_gradient_dim_1), ctypes.byref(ay_gradient_dim_2), ctypes.c_void_p(ay_gradient.ctypes.data), ctypes.byref(y_gradient_dim_1), ctypes.byref(y_gradient_dim_2), ctypes.c_void_p(y_gradient.ctypes.data), ctypes.byref(a_grads_dim_1), ctypes.byref(a_grads_dim_2), ctypes.byref(a_grads_dim_3), ctypes.c_void_p(a_grads.ctypes.data), ctypes.byref(m_grads_dim_1), ctypes.byref(m_grads_dim_2), ctypes.byref(m_grads_dim_3), ctypes.c_void_p(m_grads.ctypes.data), ctypes.byref(a_emb_temp_dim_1), ctypes.byref(a_emb_temp_dim_2), ctypes.byref(a_emb_temp_dim_3), ctypes.c_void_p(a_emb_temp.ctypes.data), ctypes.byref(m_emb_temp_dim_1), ctypes.byref(m_emb_temp_dim_2), ctypes.byref(m_emb_temp_dim_3), ctypes.c_void_p(m_emb_temp.ctypes.data), ctypes.byref(emb_outs_dim_1), ctypes.byref(emb_outs_dim_2), ctypes.c_void_p(emb_outs.ctypes.data), ctypes.byref(emb_grads_dim_1), ctypes.byref(emb_grads_dim_2), ctypes.c_void_p(emb_grads.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, ax, x, sum_squared_gradient.value, model_grad, info.value, ay_gradient, y_gradient, a_grads, m_grads, a_emb_temp, m_emb_temp, emb_outs, emb_grads

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine NORMALIZE_STEP
    
    def normalize_step(self, config, model, rwork, ax, x, y, yw):
        '''! Given the data for a single step of training, ensure the data has a normalized
!  geometry that aligns with model assumptions (linear radialization).'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "rwork"
        if ((not issubclass(type(rwork), numpy.ndarray)) or
            (not numpy.asarray(rwork).flags.f_contiguous) or
            (not (rwork.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'rwork' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            rwork = numpy.asarray(rwork, dtype=ctypes.c_float, order='F')
        rwork_dim_1 = ctypes.c_long(rwork.shape[0])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
    
        # Call C-accessible Fortran wrapper.
        clib.c_normalize_step(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(rwork_dim_1), ctypes.c_void_p(rwork.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return model, rwork, ax, x, y, yw

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine NORMALIZE_DATA
    
    def normalize_data(self, config, model, agg_iterators, ax_in, axi_in, sizes_in, x_in, xi_in, y_in, yi_in, yw_in, ax, axi, sizes, x, xi, y, yi, yw, ax_shift, ax_rescale, axi_shift, axi_rescale, ay_shift, ay_scale, x_shift, x_rescale, xi_shift, xi_rescale, y_shift, y_rescale, yi_shift, yi_rescale, a_emb_vecs, m_emb_vecs, o_emb_vecs, a_states, ay, info):
        '''! Make inputs and outputs radially symmetric (to make initialization
!  more well spaced and lower the curvature of the error gradient).'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "agg_iterators"
        if ((not issubclass(type(agg_iterators), numpy.ndarray)) or
            (not numpy.asarray(agg_iterators).flags.f_contiguous) or
            (not (agg_iterators.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'agg_iterators' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            agg_iterators = numpy.asarray(agg_iterators, dtype=ctypes.c_long, order='F')
        agg_iterators_dim_1 = ctypes.c_long(agg_iterators.shape[0])
        agg_iterators_dim_2 = ctypes.c_long(agg_iterators.shape[1])
        
        # Setting up "ax_in"
        if ((not issubclass(type(ax_in), numpy.ndarray)) or
            (not numpy.asarray(ax_in).flags.f_contiguous) or
            (not (ax_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax_in = numpy.asarray(ax_in, dtype=ctypes.c_float, order='F')
        ax_in_dim_1 = ctypes.c_long(ax_in.shape[0])
        ax_in_dim_2 = ctypes.c_long(ax_in.shape[1])
        
        # Setting up "axi_in"
        if ((not issubclass(type(axi_in), numpy.ndarray)) or
            (not numpy.asarray(axi_in).flags.f_contiguous) or
            (not (axi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi_in = numpy.asarray(axi_in, dtype=ctypes.c_long, order='F')
        axi_in_dim_1 = ctypes.c_long(axi_in.shape[0])
        axi_in_dim_2 = ctypes.c_long(axi_in.shape[1])
        
        # Setting up "sizes_in"
        if ((not issubclass(type(sizes_in), numpy.ndarray)) or
            (not numpy.asarray(sizes_in).flags.f_contiguous) or
            (not (sizes_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes_in = numpy.asarray(sizes_in, dtype=ctypes.c_long, order='F')
        sizes_in_dim_1 = ctypes.c_long(sizes_in.shape[0])
        
        # Setting up "x_in"
        if ((not issubclass(type(x_in), numpy.ndarray)) or
            (not numpy.asarray(x_in).flags.f_contiguous) or
            (not (x_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x_in = numpy.asarray(x_in, dtype=ctypes.c_float, order='F')
        x_in_dim_1 = ctypes.c_long(x_in.shape[0])
        x_in_dim_2 = ctypes.c_long(x_in.shape[1])
        
        # Setting up "xi_in"
        if ((not issubclass(type(xi_in), numpy.ndarray)) or
            (not numpy.asarray(xi_in).flags.f_contiguous) or
            (not (xi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi_in = numpy.asarray(xi_in, dtype=ctypes.c_long, order='F')
        xi_in_dim_1 = ctypes.c_long(xi_in.shape[0])
        xi_in_dim_2 = ctypes.c_long(xi_in.shape[1])
        
        # Setting up "y_in"
        if ((not issubclass(type(y_in), numpy.ndarray)) or
            (not numpy.asarray(y_in).flags.f_contiguous) or
            (not (y_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_in = numpy.asarray(y_in, dtype=ctypes.c_float, order='F')
        y_in_dim_1 = ctypes.c_long(y_in.shape[0])
        y_in_dim_2 = ctypes.c_long(y_in.shape[1])
        
        # Setting up "yi_in"
        if ((not issubclass(type(yi_in), numpy.ndarray)) or
            (not numpy.asarray(yi_in).flags.f_contiguous) or
            (not (yi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi_in = numpy.asarray(yi_in, dtype=ctypes.c_long, order='F')
        yi_in_dim_1 = ctypes.c_long(yi_in.shape[0])
        yi_in_dim_2 = ctypes.c_long(yi_in.shape[1])
        
        # Setting up "yw_in"
        if ((not issubclass(type(yw_in), numpy.ndarray)) or
            (not numpy.asarray(yw_in).flags.f_contiguous) or
            (not (yw_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw_in = numpy.asarray(yw_in, dtype=ctypes.c_float, order='F')
        yw_in_dim_1 = ctypes.c_long(yw_in.shape[0])
        yw_in_dim_2 = ctypes.c_long(yw_in.shape[1])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "axi"
        if ((not issubclass(type(axi), numpy.ndarray)) or
            (not numpy.asarray(axi).flags.f_contiguous) or
            (not (axi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi = numpy.asarray(axi, dtype=ctypes.c_long, order='F')
        axi_dim_1 = ctypes.c_long(axi.shape[0])
        axi_dim_2 = ctypes.c_long(axi.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "xi"
        if ((not issubclass(type(xi), numpy.ndarray)) or
            (not numpy.asarray(xi).flags.f_contiguous) or
            (not (xi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi = numpy.asarray(xi, dtype=ctypes.c_long, order='F')
        xi_dim_1 = ctypes.c_long(xi.shape[0])
        xi_dim_2 = ctypes.c_long(xi.shape[1])
        
        # Setting up "y"
        if ((not issubclass(type(y), numpy.ndarray)) or
            (not numpy.asarray(y).flags.f_contiguous) or
            (not (y.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y = numpy.asarray(y, dtype=ctypes.c_float, order='F')
        y_dim_1 = ctypes.c_long(y.shape[0])
        y_dim_2 = ctypes.c_long(y.shape[1])
        
        # Setting up "yi"
        if ((not issubclass(type(yi), numpy.ndarray)) or
            (not numpy.asarray(yi).flags.f_contiguous) or
            (not (yi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi = numpy.asarray(yi, dtype=ctypes.c_long, order='F')
        yi_dim_1 = ctypes.c_long(yi.shape[0])
        yi_dim_2 = ctypes.c_long(yi.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
        
        # Setting up "ax_shift"
        if ((not issubclass(type(ax_shift), numpy.ndarray)) or
            (not numpy.asarray(ax_shift).flags.f_contiguous) or
            (not (ax_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax_shift = numpy.asarray(ax_shift, dtype=ctypes.c_float, order='F')
        ax_shift_dim_1 = ctypes.c_long(ax_shift.shape[0])
        
        # Setting up "ax_rescale"
        if ((not issubclass(type(ax_rescale), numpy.ndarray)) or
            (not numpy.asarray(ax_rescale).flags.f_contiguous) or
            (not (ax_rescale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax_rescale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax_rescale = numpy.asarray(ax_rescale, dtype=ctypes.c_float, order='F')
        ax_rescale_dim_1 = ctypes.c_long(ax_rescale.shape[0])
        ax_rescale_dim_2 = ctypes.c_long(ax_rescale.shape[1])
        
        # Setting up "axi_shift"
        if ((not issubclass(type(axi_shift), numpy.ndarray)) or
            (not numpy.asarray(axi_shift).flags.f_contiguous) or
            (not (axi_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'axi_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            axi_shift = numpy.asarray(axi_shift, dtype=ctypes.c_float, order='F')
        axi_shift_dim_1 = ctypes.c_long(axi_shift.shape[0])
        
        # Setting up "axi_rescale"
        if ((not issubclass(type(axi_rescale), numpy.ndarray)) or
            (not numpy.asarray(axi_rescale).flags.f_contiguous) or
            (not (axi_rescale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'axi_rescale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            axi_rescale = numpy.asarray(axi_rescale, dtype=ctypes.c_float, order='F')
        axi_rescale_dim_1 = ctypes.c_long(axi_rescale.shape[0])
        axi_rescale_dim_2 = ctypes.c_long(axi_rescale.shape[1])
        
        # Setting up "ay_shift"
        if ((not issubclass(type(ay_shift), numpy.ndarray)) or
            (not numpy.asarray(ay_shift).flags.f_contiguous) or
            (not (ay_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay_shift = numpy.asarray(ay_shift, dtype=ctypes.c_float, order='F')
        ay_shift_dim_1 = ctypes.c_long(ay_shift.shape[0])
        
        # Setting up "ay_scale"
        if ((not issubclass(type(ay_scale), numpy.ndarray)) or
            (not numpy.asarray(ay_scale).flags.f_contiguous) or
            (not (ay_scale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay_scale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay_scale = numpy.asarray(ay_scale, dtype=ctypes.c_float, order='F')
        ay_scale_dim_1 = ctypes.c_long(ay_scale.shape[0])
        
        # Setting up "x_shift"
        if ((not issubclass(type(x_shift), numpy.ndarray)) or
            (not numpy.asarray(x_shift).flags.f_contiguous) or
            (not (x_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x_shift = numpy.asarray(x_shift, dtype=ctypes.c_float, order='F')
        x_shift_dim_1 = ctypes.c_long(x_shift.shape[0])
        
        # Setting up "x_rescale"
        if ((not issubclass(type(x_rescale), numpy.ndarray)) or
            (not numpy.asarray(x_rescale).flags.f_contiguous) or
            (not (x_rescale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x_rescale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x_rescale = numpy.asarray(x_rescale, dtype=ctypes.c_float, order='F')
        x_rescale_dim_1 = ctypes.c_long(x_rescale.shape[0])
        x_rescale_dim_2 = ctypes.c_long(x_rescale.shape[1])
        
        # Setting up "xi_shift"
        if ((not issubclass(type(xi_shift), numpy.ndarray)) or
            (not numpy.asarray(xi_shift).flags.f_contiguous) or
            (not (xi_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'xi_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            xi_shift = numpy.asarray(xi_shift, dtype=ctypes.c_float, order='F')
        xi_shift_dim_1 = ctypes.c_long(xi_shift.shape[0])
        
        # Setting up "xi_rescale"
        if ((not issubclass(type(xi_rescale), numpy.ndarray)) or
            (not numpy.asarray(xi_rescale).flags.f_contiguous) or
            (not (xi_rescale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'xi_rescale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            xi_rescale = numpy.asarray(xi_rescale, dtype=ctypes.c_float, order='F')
        xi_rescale_dim_1 = ctypes.c_long(xi_rescale.shape[0])
        xi_rescale_dim_2 = ctypes.c_long(xi_rescale.shape[1])
        
        # Setting up "y_shift"
        if ((not issubclass(type(y_shift), numpy.ndarray)) or
            (not numpy.asarray(y_shift).flags.f_contiguous) or
            (not (y_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_shift = numpy.asarray(y_shift, dtype=ctypes.c_float, order='F')
        y_shift_dim_1 = ctypes.c_long(y_shift.shape[0])
        
        # Setting up "y_rescale"
        if ((not issubclass(type(y_rescale), numpy.ndarray)) or
            (not numpy.asarray(y_rescale).flags.f_contiguous) or
            (not (y_rescale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_rescale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_rescale = numpy.asarray(y_rescale, dtype=ctypes.c_float, order='F')
        y_rescale_dim_1 = ctypes.c_long(y_rescale.shape[0])
        y_rescale_dim_2 = ctypes.c_long(y_rescale.shape[1])
        
        # Setting up "yi_shift"
        if ((not issubclass(type(yi_shift), numpy.ndarray)) or
            (not numpy.asarray(yi_shift).flags.f_contiguous) or
            (not (yi_shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yi_shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yi_shift = numpy.asarray(yi_shift, dtype=ctypes.c_float, order='F')
        yi_shift_dim_1 = ctypes.c_long(yi_shift.shape[0])
        
        # Setting up "yi_rescale"
        if ((not issubclass(type(yi_rescale), numpy.ndarray)) or
            (not numpy.asarray(yi_rescale).flags.f_contiguous) or
            (not (yi_rescale.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yi_rescale' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yi_rescale = numpy.asarray(yi_rescale, dtype=ctypes.c_float, order='F')
        yi_rescale_dim_1 = ctypes.c_long(yi_rescale.shape[0])
        yi_rescale_dim_2 = ctypes.c_long(yi_rescale.shape[1])
        
        # Setting up "a_emb_vecs"
        if ((not issubclass(type(a_emb_vecs), numpy.ndarray)) or
            (not numpy.asarray(a_emb_vecs).flags.f_contiguous) or
            (not (a_emb_vecs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_emb_vecs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_emb_vecs = numpy.asarray(a_emb_vecs, dtype=ctypes.c_float, order='F')
        a_emb_vecs_dim_1 = ctypes.c_long(a_emb_vecs.shape[0])
        a_emb_vecs_dim_2 = ctypes.c_long(a_emb_vecs.shape[1])
        
        # Setting up "m_emb_vecs"
        if ((not issubclass(type(m_emb_vecs), numpy.ndarray)) or
            (not numpy.asarray(m_emb_vecs).flags.f_contiguous) or
            (not (m_emb_vecs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_emb_vecs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_emb_vecs = numpy.asarray(m_emb_vecs, dtype=ctypes.c_float, order='F')
        m_emb_vecs_dim_1 = ctypes.c_long(m_emb_vecs.shape[0])
        m_emb_vecs_dim_2 = ctypes.c_long(m_emb_vecs.shape[1])
        
        # Setting up "o_emb_vecs"
        if ((not issubclass(type(o_emb_vecs), numpy.ndarray)) or
            (not numpy.asarray(o_emb_vecs).flags.f_contiguous) or
            (not (o_emb_vecs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'o_emb_vecs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            o_emb_vecs = numpy.asarray(o_emb_vecs, dtype=ctypes.c_float, order='F')
        o_emb_vecs_dim_1 = ctypes.c_long(o_emb_vecs.shape[0])
        o_emb_vecs_dim_2 = ctypes.c_long(o_emb_vecs.shape[1])
        
        # Setting up "a_states"
        if ((not issubclass(type(a_states), numpy.ndarray)) or
            (not numpy.asarray(a_states).flags.f_contiguous) or
            (not (a_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_states = numpy.asarray(a_states, dtype=ctypes.c_float, order='F')
        a_states_dim_1 = ctypes.c_long(a_states.shape[0])
        a_states_dim_2 = ctypes.c_long(a_states.shape[1])
        a_states_dim_3 = ctypes.c_long(a_states.shape[2])
        
        # Setting up "ay"
        if ((not issubclass(type(ay), numpy.ndarray)) or
            (not numpy.asarray(ay).flags.f_contiguous) or
            (not (ay.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay = numpy.asarray(ay, dtype=ctypes.c_float, order='F')
        ay_dim_1 = ctypes.c_long(ay.shape[0])
        ay_dim_2 = ctypes.c_long(ay.shape[1])
        
        # Setting up "info"
        if (type(info) is not ctypes.c_int): info = ctypes.c_int(info)
    
        # Call C-accessible Fortran wrapper.
        clib.c_normalize_data(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(agg_iterators_dim_1), ctypes.byref(agg_iterators_dim_2), ctypes.c_void_p(agg_iterators.ctypes.data), ctypes.byref(ax_in_dim_1), ctypes.byref(ax_in_dim_2), ctypes.c_void_p(ax_in.ctypes.data), ctypes.byref(axi_in_dim_1), ctypes.byref(axi_in_dim_2), ctypes.c_void_p(axi_in.ctypes.data), ctypes.byref(sizes_in_dim_1), ctypes.c_void_p(sizes_in.ctypes.data), ctypes.byref(x_in_dim_1), ctypes.byref(x_in_dim_2), ctypes.c_void_p(x_in.ctypes.data), ctypes.byref(xi_in_dim_1), ctypes.byref(xi_in_dim_2), ctypes.c_void_p(xi_in.ctypes.data), ctypes.byref(y_in_dim_1), ctypes.byref(y_in_dim_2), ctypes.c_void_p(y_in.ctypes.data), ctypes.byref(yi_in_dim_1), ctypes.byref(yi_in_dim_2), ctypes.c_void_p(yi_in.ctypes.data), ctypes.byref(yw_in_dim_1), ctypes.byref(yw_in_dim_2), ctypes.c_void_p(yw_in.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(axi_dim_1), ctypes.byref(axi_dim_2), ctypes.c_void_p(axi.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(xi_dim_1), ctypes.byref(xi_dim_2), ctypes.c_void_p(xi.ctypes.data), ctypes.byref(y_dim_1), ctypes.byref(y_dim_2), ctypes.c_void_p(y.ctypes.data), ctypes.byref(yi_dim_1), ctypes.byref(yi_dim_2), ctypes.c_void_p(yi.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data), ctypes.byref(ax_shift_dim_1), ctypes.c_void_p(ax_shift.ctypes.data), ctypes.byref(ax_rescale_dim_1), ctypes.byref(ax_rescale_dim_2), ctypes.c_void_p(ax_rescale.ctypes.data), ctypes.byref(axi_shift_dim_1), ctypes.c_void_p(axi_shift.ctypes.data), ctypes.byref(axi_rescale_dim_1), ctypes.byref(axi_rescale_dim_2), ctypes.c_void_p(axi_rescale.ctypes.data), ctypes.byref(ay_shift_dim_1), ctypes.c_void_p(ay_shift.ctypes.data), ctypes.byref(ay_scale_dim_1), ctypes.c_void_p(ay_scale.ctypes.data), ctypes.byref(x_shift_dim_1), ctypes.c_void_p(x_shift.ctypes.data), ctypes.byref(x_rescale_dim_1), ctypes.byref(x_rescale_dim_2), ctypes.c_void_p(x_rescale.ctypes.data), ctypes.byref(xi_shift_dim_1), ctypes.c_void_p(xi_shift.ctypes.data), ctypes.byref(xi_rescale_dim_1), ctypes.byref(xi_rescale_dim_2), ctypes.c_void_p(xi_rescale.ctypes.data), ctypes.byref(y_shift_dim_1), ctypes.c_void_p(y_shift.ctypes.data), ctypes.byref(y_rescale_dim_1), ctypes.byref(y_rescale_dim_2), ctypes.c_void_p(y_rescale.ctypes.data), ctypes.byref(yi_shift_dim_1), ctypes.c_void_p(yi_shift.ctypes.data), ctypes.byref(yi_rescale_dim_1), ctypes.byref(yi_rescale_dim_2), ctypes.c_void_p(yi_rescale.ctypes.data), ctypes.byref(a_emb_vecs_dim_1), ctypes.byref(a_emb_vecs_dim_2), ctypes.c_void_p(a_emb_vecs.ctypes.data), ctypes.byref(m_emb_vecs_dim_1), ctypes.byref(m_emb_vecs_dim_2), ctypes.c_void_p(m_emb_vecs.ctypes.data), ctypes.byref(o_emb_vecs_dim_1), ctypes.byref(o_emb_vecs_dim_2), ctypes.c_void_p(o_emb_vecs.ctypes.data), ctypes.byref(a_states_dim_1), ctypes.byref(a_states_dim_2), ctypes.byref(a_states_dim_3), ctypes.c_void_p(a_states.ctypes.data), ctypes.byref(ay_dim_1), ctypes.byref(ay_dim_2), ctypes.c_void_p(ay.ctypes.data), ctypes.byref(info))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, model, agg_iterators, ax_in, x_in, y_in, yw_in, ax, axi, sizes, x, xi, y, yi, yw, ax_shift, ax_rescale, axi_shift, axi_rescale, ay_shift, ay_scale, x_shift, x_rescale, xi_shift, xi_rescale, y_shift, y_rescale, yi_shift, yi_rescale, a_emb_vecs, m_emb_vecs, o_emb_vecs, a_states, ay, info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine CONDITION_MODEL
    
    def condition_model(self, config, model, model_grad_mean, model_grad_curv, ax, axi, ay, ay_gradient, sizes, x, xi, y_gradient, num_threads, fit_step, a_states, m_states, a_grads, m_grads, a_lengths, m_lengths, a_state_temp, m_state_temp, a_order, m_order, total_eval_rank, total_grad_rank):
        '''! Performing conditioning related operations on this model
!  (ensure that mean squared error is reducible).'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "model_grad_mean"
        if ((not issubclass(type(model_grad_mean), numpy.ndarray)) or
            (not numpy.asarray(model_grad_mean).flags.f_contiguous) or
            (not (model_grad_mean.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model_grad_mean' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model_grad_mean = numpy.asarray(model_grad_mean, dtype=ctypes.c_float, order='F')
        model_grad_mean_dim_1 = ctypes.c_long(model_grad_mean.shape[0])
        
        # Setting up "model_grad_curv"
        if ((not issubclass(type(model_grad_curv), numpy.ndarray)) or
            (not numpy.asarray(model_grad_curv).flags.f_contiguous) or
            (not (model_grad_curv.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model_grad_curv' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model_grad_curv = numpy.asarray(model_grad_curv, dtype=ctypes.c_float, order='F')
        model_grad_curv_dim_1 = ctypes.c_long(model_grad_curv.shape[0])
        
        # Setting up "ax"
        if ((not issubclass(type(ax), numpy.ndarray)) or
            (not numpy.asarray(ax).flags.f_contiguous) or
            (not (ax.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax = numpy.asarray(ax, dtype=ctypes.c_float, order='F')
        ax_dim_1 = ctypes.c_long(ax.shape[0])
        ax_dim_2 = ctypes.c_long(ax.shape[1])
        
        # Setting up "axi"
        if ((not issubclass(type(axi), numpy.ndarray)) or
            (not numpy.asarray(axi).flags.f_contiguous) or
            (not (axi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi = numpy.asarray(axi, dtype=ctypes.c_long, order='F')
        axi_dim_1 = ctypes.c_long(axi.shape[0])
        axi_dim_2 = ctypes.c_long(axi.shape[1])
        
        # Setting up "ay"
        if ((not issubclass(type(ay), numpy.ndarray)) or
            (not numpy.asarray(ay).flags.f_contiguous) or
            (not (ay.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay = numpy.asarray(ay, dtype=ctypes.c_float, order='F')
        ay_dim_1 = ctypes.c_long(ay.shape[0])
        ay_dim_2 = ctypes.c_long(ay.shape[1])
        
        # Setting up "ay_gradient"
        if ((not issubclass(type(ay_gradient), numpy.ndarray)) or
            (not numpy.asarray(ay_gradient).flags.f_contiguous) or
            (not (ay_gradient.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ay_gradient' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ay_gradient = numpy.asarray(ay_gradient, dtype=ctypes.c_float, order='F')
        ay_gradient_dim_1 = ctypes.c_long(ay_gradient.shape[0])
        ay_gradient_dim_2 = ctypes.c_long(ay_gradient.shape[1])
        
        # Setting up "sizes"
        if ((not issubclass(type(sizes), numpy.ndarray)) or
            (not numpy.asarray(sizes).flags.f_contiguous) or
            (not (sizes.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes = numpy.asarray(sizes, dtype=ctypes.c_long, order='F')
        sizes_dim_1 = ctypes.c_long(sizes.shape[0])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "xi"
        if ((not issubclass(type(xi), numpy.ndarray)) or
            (not numpy.asarray(xi).flags.f_contiguous) or
            (not (xi.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi = numpy.asarray(xi, dtype=ctypes.c_long, order='F')
        xi_dim_1 = ctypes.c_long(xi.shape[0])
        xi_dim_2 = ctypes.c_long(xi.shape[1])
        
        # Setting up "y_gradient"
        if ((not issubclass(type(y_gradient), numpy.ndarray)) or
            (not numpy.asarray(y_gradient).flags.f_contiguous) or
            (not (y_gradient.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_gradient' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_gradient = numpy.asarray(y_gradient, dtype=ctypes.c_float, order='F')
        y_gradient_dim_1 = ctypes.c_long(y_gradient.shape[0])
        y_gradient_dim_2 = ctypes.c_long(y_gradient.shape[1])
        
        # Setting up "num_threads"
        if (type(num_threads) is not ctypes.c_long): num_threads = ctypes.c_long(num_threads)
        
        # Setting up "fit_step"
        if (type(fit_step) is not ctypes.c_long): fit_step = ctypes.c_long(fit_step)
        
        # Setting up "a_states"
        if ((not issubclass(type(a_states), numpy.ndarray)) or
            (not numpy.asarray(a_states).flags.f_contiguous) or
            (not (a_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_states = numpy.asarray(a_states, dtype=ctypes.c_float, order='F')
        a_states_dim_1 = ctypes.c_long(a_states.shape[0])
        a_states_dim_2 = ctypes.c_long(a_states.shape[1])
        a_states_dim_3 = ctypes.c_long(a_states.shape[2])
        
        # Setting up "m_states"
        if ((not issubclass(type(m_states), numpy.ndarray)) or
            (not numpy.asarray(m_states).flags.f_contiguous) or
            (not (m_states.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_states' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_states = numpy.asarray(m_states, dtype=ctypes.c_float, order='F')
        m_states_dim_1 = ctypes.c_long(m_states.shape[0])
        m_states_dim_2 = ctypes.c_long(m_states.shape[1])
        m_states_dim_3 = ctypes.c_long(m_states.shape[2])
        
        # Setting up "a_grads"
        if ((not issubclass(type(a_grads), numpy.ndarray)) or
            (not numpy.asarray(a_grads).flags.f_contiguous) or
            (not (a_grads.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_grads' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_grads = numpy.asarray(a_grads, dtype=ctypes.c_float, order='F')
        a_grads_dim_1 = ctypes.c_long(a_grads.shape[0])
        a_grads_dim_2 = ctypes.c_long(a_grads.shape[1])
        a_grads_dim_3 = ctypes.c_long(a_grads.shape[2])
        
        # Setting up "m_grads"
        if ((not issubclass(type(m_grads), numpy.ndarray)) or
            (not numpy.asarray(m_grads).flags.f_contiguous) or
            (not (m_grads.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_grads' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_grads = numpy.asarray(m_grads, dtype=ctypes.c_float, order='F')
        m_grads_dim_1 = ctypes.c_long(m_grads.shape[0])
        m_grads_dim_2 = ctypes.c_long(m_grads.shape[1])
        m_grads_dim_3 = ctypes.c_long(m_grads.shape[2])
        
        # Setting up "a_lengths"
        if ((not issubclass(type(a_lengths), numpy.ndarray)) or
            (not numpy.asarray(a_lengths).flags.f_contiguous) or
            (not (a_lengths.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_lengths' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_lengths = numpy.asarray(a_lengths, dtype=ctypes.c_float, order='F')
        a_lengths_dim_1 = ctypes.c_long(a_lengths.shape[0])
        a_lengths_dim_2 = ctypes.c_long(a_lengths.shape[1])
        
        # Setting up "m_lengths"
        if ((not issubclass(type(m_lengths), numpy.ndarray)) or
            (not numpy.asarray(m_lengths).flags.f_contiguous) or
            (not (m_lengths.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_lengths' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_lengths = numpy.asarray(m_lengths, dtype=ctypes.c_float, order='F')
        m_lengths_dim_1 = ctypes.c_long(m_lengths.shape[0])
        m_lengths_dim_2 = ctypes.c_long(m_lengths.shape[1])
        
        # Setting up "a_state_temp"
        if ((not issubclass(type(a_state_temp), numpy.ndarray)) or
            (not numpy.asarray(a_state_temp).flags.f_contiguous) or
            (not (a_state_temp.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a_state_temp' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a_state_temp = numpy.asarray(a_state_temp, dtype=ctypes.c_float, order='F')
        a_state_temp_dim_1 = ctypes.c_long(a_state_temp.shape[0])
        a_state_temp_dim_2 = ctypes.c_long(a_state_temp.shape[1])
        
        # Setting up "m_state_temp"
        if ((not issubclass(type(m_state_temp), numpy.ndarray)) or
            (not numpy.asarray(m_state_temp).flags.f_contiguous) or
            (not (m_state_temp.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'm_state_temp' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            m_state_temp = numpy.asarray(m_state_temp, dtype=ctypes.c_float, order='F')
        m_state_temp_dim_1 = ctypes.c_long(m_state_temp.shape[0])
        m_state_temp_dim_2 = ctypes.c_long(m_state_temp.shape[1])
        
        # Setting up "a_order"
        if ((not issubclass(type(a_order), numpy.ndarray)) or
            (not numpy.asarray(a_order).flags.f_contiguous) or
            (not (a_order.dtype == numpy.dtype(ctypes.c_int)))):
            import warnings
            warnings.warn("The provided argument 'a_order' was not an f_contiguous NumPy array of type 'ctypes.c_int' (or equivalent). Automatically converting (probably creating a full copy).")
            a_order = numpy.asarray(a_order, dtype=ctypes.c_int, order='F')
        a_order_dim_1 = ctypes.c_long(a_order.shape[0])
        a_order_dim_2 = ctypes.c_long(a_order.shape[1])
        
        # Setting up "m_order"
        if ((not issubclass(type(m_order), numpy.ndarray)) or
            (not numpy.asarray(m_order).flags.f_contiguous) or
            (not (m_order.dtype == numpy.dtype(ctypes.c_int)))):
            import warnings
            warnings.warn("The provided argument 'm_order' was not an f_contiguous NumPy array of type 'ctypes.c_int' (or equivalent). Automatically converting (probably creating a full copy).")
            m_order = numpy.asarray(m_order, dtype=ctypes.c_int, order='F')
        m_order_dim_1 = ctypes.c_long(m_order.shape[0])
        m_order_dim_2 = ctypes.c_long(m_order.shape[1])
        
        # Setting up "total_eval_rank"
        if (type(total_eval_rank) is not ctypes.c_int): total_eval_rank = ctypes.c_int(total_eval_rank)
        
        # Setting up "total_grad_rank"
        if (type(total_grad_rank) is not ctypes.c_int): total_grad_rank = ctypes.c_int(total_grad_rank)
    
        # Call C-accessible Fortran wrapper.
        clib.c_condition_model(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(model_grad_mean_dim_1), ctypes.c_void_p(model_grad_mean.ctypes.data), ctypes.byref(model_grad_curv_dim_1), ctypes.c_void_p(model_grad_curv.ctypes.data), ctypes.byref(ax_dim_1), ctypes.byref(ax_dim_2), ctypes.c_void_p(ax.ctypes.data), ctypes.byref(axi_dim_1), ctypes.byref(axi_dim_2), ctypes.c_void_p(axi.ctypes.data), ctypes.byref(ay_dim_1), ctypes.byref(ay_dim_2), ctypes.c_void_p(ay.ctypes.data), ctypes.byref(ay_gradient_dim_1), ctypes.byref(ay_gradient_dim_2), ctypes.c_void_p(ay_gradient.ctypes.data), ctypes.byref(sizes_dim_1), ctypes.c_void_p(sizes.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(xi_dim_1), ctypes.byref(xi_dim_2), ctypes.c_void_p(xi.ctypes.data), ctypes.byref(y_gradient_dim_1), ctypes.byref(y_gradient_dim_2), ctypes.c_void_p(y_gradient.ctypes.data), ctypes.byref(num_threads), ctypes.byref(fit_step), ctypes.byref(a_states_dim_1), ctypes.byref(a_states_dim_2), ctypes.byref(a_states_dim_3), ctypes.c_void_p(a_states.ctypes.data), ctypes.byref(m_states_dim_1), ctypes.byref(m_states_dim_2), ctypes.byref(m_states_dim_3), ctypes.c_void_p(m_states.ctypes.data), ctypes.byref(a_grads_dim_1), ctypes.byref(a_grads_dim_2), ctypes.byref(a_grads_dim_3), ctypes.c_void_p(a_grads.ctypes.data), ctypes.byref(m_grads_dim_1), ctypes.byref(m_grads_dim_2), ctypes.byref(m_grads_dim_3), ctypes.c_void_p(m_grads.ctypes.data), ctypes.byref(a_lengths_dim_1), ctypes.byref(a_lengths_dim_2), ctypes.c_void_p(a_lengths.ctypes.data), ctypes.byref(m_lengths_dim_1), ctypes.byref(m_lengths_dim_2), ctypes.c_void_p(m_lengths.ctypes.data), ctypes.byref(a_state_temp_dim_1), ctypes.byref(a_state_temp_dim_2), ctypes.c_void_p(a_state_temp.ctypes.data), ctypes.byref(m_state_temp_dim_1), ctypes.byref(m_state_temp_dim_2), ctypes.c_void_p(m_state_temp.ctypes.data), ctypes.byref(a_order_dim_1), ctypes.byref(a_order_dim_2), ctypes.c_void_p(a_order.ctypes.data), ctypes.byref(m_order_dim_1), ctypes.byref(m_order_dim_2), ctypes.c_void_p(m_order.ctypes.data), ctypes.byref(total_eval_rank), ctypes.byref(total_grad_rank))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, model, model_grad_mean, model_grad_curv, ax, x, a_states, m_states, a_grads, m_grads, a_lengths, m_lengths, a_state_temp, m_state_temp, a_order, m_order, total_eval_rank.value, total_grad_rank.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine FIT_CHECK
    
    def fit_check(self, config, model, rwork, iwork, lwork, ax_in, axi_in, sizes_in, x_in, xi_in, y_in, yi_in, yw_in, yw, agg_iterators):
        '''! Check all of the same inputs for FIT_MODEL to make sure shapes ane sizes match.
! TODO: Take an output file name (STDERR and STDOUT are handled).'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "rwork"
        if ((not issubclass(type(rwork), numpy.ndarray)) or
            (not numpy.asarray(rwork).flags.f_contiguous) or
            (not (rwork.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'rwork' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            rwork = numpy.asarray(rwork, dtype=ctypes.c_float, order='F')
        rwork_dim_1 = ctypes.c_long(rwork.shape[0])
        
        # Setting up "iwork"
        if ((not issubclass(type(iwork), numpy.ndarray)) or
            (not numpy.asarray(iwork).flags.f_contiguous) or
            (not (iwork.dtype == numpy.dtype(ctypes.c_int)))):
            import warnings
            warnings.warn("The provided argument 'iwork' was not an f_contiguous NumPy array of type 'ctypes.c_int' (or equivalent). Automatically converting (probably creating a full copy).")
            iwork = numpy.asarray(iwork, dtype=ctypes.c_int, order='F')
        iwork_dim_1 = ctypes.c_long(iwork.shape[0])
        
        # Setting up "lwork"
        if ((not issubclass(type(lwork), numpy.ndarray)) or
            (not numpy.asarray(lwork).flags.f_contiguous) or
            (not (lwork.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'lwork' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            lwork = numpy.asarray(lwork, dtype=ctypes.c_long, order='F')
        lwork_dim_1 = ctypes.c_long(lwork.shape[0])
        
        # Setting up "ax_in"
        if ((not issubclass(type(ax_in), numpy.ndarray)) or
            (not numpy.asarray(ax_in).flags.f_contiguous) or
            (not (ax_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax_in = numpy.asarray(ax_in, dtype=ctypes.c_float, order='F')
        ax_in_dim_1 = ctypes.c_long(ax_in.shape[0])
        ax_in_dim_2 = ctypes.c_long(ax_in.shape[1])
        
        # Setting up "axi_in"
        if ((not issubclass(type(axi_in), numpy.ndarray)) or
            (not numpy.asarray(axi_in).flags.f_contiguous) or
            (not (axi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi_in = numpy.asarray(axi_in, dtype=ctypes.c_long, order='F')
        axi_in_dim_1 = ctypes.c_long(axi_in.shape[0])
        axi_in_dim_2 = ctypes.c_long(axi_in.shape[1])
        
        # Setting up "sizes_in"
        if ((not issubclass(type(sizes_in), numpy.ndarray)) or
            (not numpy.asarray(sizes_in).flags.f_contiguous) or
            (not (sizes_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes_in = numpy.asarray(sizes_in, dtype=ctypes.c_long, order='F')
        sizes_in_dim_1 = ctypes.c_long(sizes_in.shape[0])
        
        # Setting up "x_in"
        if ((not issubclass(type(x_in), numpy.ndarray)) or
            (not numpy.asarray(x_in).flags.f_contiguous) or
            (not (x_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x_in = numpy.asarray(x_in, dtype=ctypes.c_float, order='F')
        x_in_dim_1 = ctypes.c_long(x_in.shape[0])
        x_in_dim_2 = ctypes.c_long(x_in.shape[1])
        
        # Setting up "xi_in"
        if ((not issubclass(type(xi_in), numpy.ndarray)) or
            (not numpy.asarray(xi_in).flags.f_contiguous) or
            (not (xi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi_in = numpy.asarray(xi_in, dtype=ctypes.c_long, order='F')
        xi_in_dim_1 = ctypes.c_long(xi_in.shape[0])
        xi_in_dim_2 = ctypes.c_long(xi_in.shape[1])
        
        # Setting up "y_in"
        if ((not issubclass(type(y_in), numpy.ndarray)) or
            (not numpy.asarray(y_in).flags.f_contiguous) or
            (not (y_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_in = numpy.asarray(y_in, dtype=ctypes.c_float, order='F')
        y_in_dim_1 = ctypes.c_long(y_in.shape[0])
        y_in_dim_2 = ctypes.c_long(y_in.shape[1])
        
        # Setting up "yi_in"
        if ((not issubclass(type(yi_in), numpy.ndarray)) or
            (not numpy.asarray(yi_in).flags.f_contiguous) or
            (not (yi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi_in = numpy.asarray(yi_in, dtype=ctypes.c_long, order='F')
        yi_in_dim_1 = ctypes.c_long(yi_in.shape[0])
        yi_in_dim_2 = ctypes.c_long(yi_in.shape[1])
        
        # Setting up "yw_in"
        if ((not issubclass(type(yw_in), numpy.ndarray)) or
            (not numpy.asarray(yw_in).flags.f_contiguous) or
            (not (yw_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw_in = numpy.asarray(yw_in, dtype=ctypes.c_float, order='F')
        yw_in_dim_1 = ctypes.c_long(yw_in.shape[0])
        yw_in_dim_2 = ctypes.c_long(yw_in.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
        
        # Setting up "agg_iterators"
        if ((not issubclass(type(agg_iterators), numpy.ndarray)) or
            (not numpy.asarray(agg_iterators).flags.f_contiguous) or
            (not (agg_iterators.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'agg_iterators' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            agg_iterators = numpy.asarray(agg_iterators, dtype=ctypes.c_long, order='F')
        agg_iterators_dim_1 = ctypes.c_long(agg_iterators.shape[0])
        agg_iterators_dim_2 = ctypes.c_long(agg_iterators.shape[1])
        
        # Setting up "info"
        info = ctypes.c_int()
    
        # Call C-accessible Fortran wrapper.
        clib.c_fit_check(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(rwork_dim_1), ctypes.c_void_p(rwork.ctypes.data), ctypes.byref(iwork_dim_1), ctypes.c_void_p(iwork.ctypes.data), ctypes.byref(lwork_dim_1), ctypes.c_void_p(lwork.ctypes.data), ctypes.byref(ax_in_dim_1), ctypes.byref(ax_in_dim_2), ctypes.c_void_p(ax_in.ctypes.data), ctypes.byref(axi_in_dim_1), ctypes.byref(axi_in_dim_2), ctypes.c_void_p(axi_in.ctypes.data), ctypes.byref(sizes_in_dim_1), ctypes.c_void_p(sizes_in.ctypes.data), ctypes.byref(x_in_dim_1), ctypes.byref(x_in_dim_2), ctypes.c_void_p(x_in.ctypes.data), ctypes.byref(xi_in_dim_1), ctypes.byref(xi_in_dim_2), ctypes.c_void_p(xi_in.ctypes.data), ctypes.byref(y_in_dim_1), ctypes.byref(y_in_dim_2), ctypes.c_void_p(y_in.ctypes.data), ctypes.byref(yi_in_dim_1), ctypes.byref(yi_in_dim_2), ctypes.c_void_p(yi_in.ctypes.data), ctypes.byref(yw_in_dim_1), ctypes.byref(yw_in_dim_2), ctypes.c_void_p(yw_in.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data), ctypes.byref(agg_iterators_dim_1), ctypes.byref(agg_iterators_dim_2), ctypes.c_void_p(agg_iterators.ctypes.data), ctypes.byref(info))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine FIT_MODEL
    
    def fit_model(self, config, model, rwork, iwork, lwork, ax_in, axi_in, sizes_in, x_in, xi_in, y_in, yi_in, yw_in, yw, agg_iterators, steps, record=None, continuing=None):
        '''! Fit input / output pairs by minimizing mean squared error.
! TODO: Take an output file name (STDERR and STDOUT are handled).'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "config"
        if (type(config) is not MODEL_CONFIG): config = MODEL_CONFIG(config)
        
        # Setting up "model"
        if ((not issubclass(type(model), numpy.ndarray)) or
            (not numpy.asarray(model).flags.f_contiguous) or
            (not (model.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'model' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            model = numpy.asarray(model, dtype=ctypes.c_float, order='F')
        model_dim_1 = ctypes.c_long(model.shape[0])
        
        # Setting up "rwork"
        if ((not issubclass(type(rwork), numpy.ndarray)) or
            (not numpy.asarray(rwork).flags.f_contiguous) or
            (not (rwork.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'rwork' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            rwork = numpy.asarray(rwork, dtype=ctypes.c_float, order='F')
        rwork_dim_1 = ctypes.c_long(rwork.shape[0])
        
        # Setting up "iwork"
        if ((not issubclass(type(iwork), numpy.ndarray)) or
            (not numpy.asarray(iwork).flags.f_contiguous) or
            (not (iwork.dtype == numpy.dtype(ctypes.c_int)))):
            import warnings
            warnings.warn("The provided argument 'iwork' was not an f_contiguous NumPy array of type 'ctypes.c_int' (or equivalent). Automatically converting (probably creating a full copy).")
            iwork = numpy.asarray(iwork, dtype=ctypes.c_int, order='F')
        iwork_dim_1 = ctypes.c_long(iwork.shape[0])
        
        # Setting up "lwork"
        if ((not issubclass(type(lwork), numpy.ndarray)) or
            (not numpy.asarray(lwork).flags.f_contiguous) or
            (not (lwork.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'lwork' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            lwork = numpy.asarray(lwork, dtype=ctypes.c_long, order='F')
        lwork_dim_1 = ctypes.c_long(lwork.shape[0])
        
        # Setting up "ax_in"
        if ((not issubclass(type(ax_in), numpy.ndarray)) or
            (not numpy.asarray(ax_in).flags.f_contiguous) or
            (not (ax_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'ax_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            ax_in = numpy.asarray(ax_in, dtype=ctypes.c_float, order='F')
        ax_in_dim_1 = ctypes.c_long(ax_in.shape[0])
        ax_in_dim_2 = ctypes.c_long(ax_in.shape[1])
        
        # Setting up "axi_in"
        if ((not issubclass(type(axi_in), numpy.ndarray)) or
            (not numpy.asarray(axi_in).flags.f_contiguous) or
            (not (axi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'axi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            axi_in = numpy.asarray(axi_in, dtype=ctypes.c_long, order='F')
        axi_in_dim_1 = ctypes.c_long(axi_in.shape[0])
        axi_in_dim_2 = ctypes.c_long(axi_in.shape[1])
        
        # Setting up "sizes_in"
        if ((not issubclass(type(sizes_in), numpy.ndarray)) or
            (not numpy.asarray(sizes_in).flags.f_contiguous) or
            (not (sizes_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'sizes_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            sizes_in = numpy.asarray(sizes_in, dtype=ctypes.c_long, order='F')
        sizes_in_dim_1 = ctypes.c_long(sizes_in.shape[0])
        
        # Setting up "x_in"
        if ((not issubclass(type(x_in), numpy.ndarray)) or
            (not numpy.asarray(x_in).flags.f_contiguous) or
            (not (x_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x_in = numpy.asarray(x_in, dtype=ctypes.c_float, order='F')
        x_in_dim_1 = ctypes.c_long(x_in.shape[0])
        x_in_dim_2 = ctypes.c_long(x_in.shape[1])
        
        # Setting up "xi_in"
        if ((not issubclass(type(xi_in), numpy.ndarray)) or
            (not numpy.asarray(xi_in).flags.f_contiguous) or
            (not (xi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'xi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            xi_in = numpy.asarray(xi_in, dtype=ctypes.c_long, order='F')
        xi_in_dim_1 = ctypes.c_long(xi_in.shape[0])
        xi_in_dim_2 = ctypes.c_long(xi_in.shape[1])
        
        # Setting up "y_in"
        if ((not issubclass(type(y_in), numpy.ndarray)) or
            (not numpy.asarray(y_in).flags.f_contiguous) or
            (not (y_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'y_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            y_in = numpy.asarray(y_in, dtype=ctypes.c_float, order='F')
        y_in_dim_1 = ctypes.c_long(y_in.shape[0])
        y_in_dim_2 = ctypes.c_long(y_in.shape[1])
        
        # Setting up "yi_in"
        if ((not issubclass(type(yi_in), numpy.ndarray)) or
            (not numpy.asarray(yi_in).flags.f_contiguous) or
            (not (yi_in.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'yi_in' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            yi_in = numpy.asarray(yi_in, dtype=ctypes.c_long, order='F')
        yi_in_dim_1 = ctypes.c_long(yi_in.shape[0])
        yi_in_dim_2 = ctypes.c_long(yi_in.shape[1])
        
        # Setting up "yw_in"
        if ((not issubclass(type(yw_in), numpy.ndarray)) or
            (not numpy.asarray(yw_in).flags.f_contiguous) or
            (not (yw_in.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw_in' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw_in = numpy.asarray(yw_in, dtype=ctypes.c_float, order='F')
        yw_in_dim_1 = ctypes.c_long(yw_in.shape[0])
        yw_in_dim_2 = ctypes.c_long(yw_in.shape[1])
        
        # Setting up "yw"
        if ((not issubclass(type(yw), numpy.ndarray)) or
            (not numpy.asarray(yw).flags.f_contiguous) or
            (not (yw.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'yw' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            yw = numpy.asarray(yw, dtype=ctypes.c_float, order='F')
        yw_dim_1 = ctypes.c_long(yw.shape[0])
        yw_dim_2 = ctypes.c_long(yw.shape[1])
        
        # Setting up "agg_iterators"
        if ((not issubclass(type(agg_iterators), numpy.ndarray)) or
            (not numpy.asarray(agg_iterators).flags.f_contiguous) or
            (not (agg_iterators.dtype == numpy.dtype(ctypes.c_long)))):
            import warnings
            warnings.warn("The provided argument 'agg_iterators' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
            agg_iterators = numpy.asarray(agg_iterators, dtype=ctypes.c_long, order='F')
        agg_iterators_dim_1 = ctypes.c_long(agg_iterators.shape[0])
        agg_iterators_dim_2 = ctypes.c_long(agg_iterators.shape[1])
        
        # Setting up "steps"
        if (type(steps) is not ctypes.c_int): steps = ctypes.c_int(steps)
        
        # Setting up "record"
        record_present = ctypes.c_bool(True)
        if (record is None):
            record_present = ctypes.c_bool(False)
            record = numpy.zeros(shape=(1,1), dtype=ctypes.c_float, order='F')
        elif (type(record) == bool) and (record):
            record = numpy.zeros(shape=(6, steps), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(record), numpy.ndarray)) or
              (not numpy.asarray(record).flags.f_contiguous) or
              (not (record.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'record' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            record = numpy.asarray(record, dtype=ctypes.c_float, order='F')
        if (record_present):
            record_dim_1 = ctypes.c_long(record.shape[0])
            record_dim_2 = ctypes.c_long(record.shape[1])
        else:
            record_dim_1 = ctypes.c_long()
            record_dim_2 = ctypes.c_long()
        
        # Setting up "sum_squared_error"
        sum_squared_error = ctypes.c_float()
        
        # Setting up "continuing"
        continuing_present = ctypes.c_bool(True)
        if (continuing is None):
            continuing_present = ctypes.c_bool(False)
            continuing = ctypes.c_bool()
        else:
            continuing = ctypes.c_bool(continuing)
        if (type(continuing) is not ctypes.c_bool): continuing = ctypes.c_bool(continuing)
        
        # Setting up "info"
        info = ctypes.c_int()
    
        # Call C-accessible Fortran wrapper.
        clib.c_fit_model(ctypes.byref(config), ctypes.byref(model_dim_1), ctypes.c_void_p(model.ctypes.data), ctypes.byref(rwork_dim_1), ctypes.c_void_p(rwork.ctypes.data), ctypes.byref(iwork_dim_1), ctypes.c_void_p(iwork.ctypes.data), ctypes.byref(lwork_dim_1), ctypes.c_void_p(lwork.ctypes.data), ctypes.byref(ax_in_dim_1), ctypes.byref(ax_in_dim_2), ctypes.c_void_p(ax_in.ctypes.data), ctypes.byref(axi_in_dim_1), ctypes.byref(axi_in_dim_2), ctypes.c_void_p(axi_in.ctypes.data), ctypes.byref(sizes_in_dim_1), ctypes.c_void_p(sizes_in.ctypes.data), ctypes.byref(x_in_dim_1), ctypes.byref(x_in_dim_2), ctypes.c_void_p(x_in.ctypes.data), ctypes.byref(xi_in_dim_1), ctypes.byref(xi_in_dim_2), ctypes.c_void_p(xi_in.ctypes.data), ctypes.byref(y_in_dim_1), ctypes.byref(y_in_dim_2), ctypes.c_void_p(y_in.ctypes.data), ctypes.byref(yi_in_dim_1), ctypes.byref(yi_in_dim_2), ctypes.c_void_p(yi_in.ctypes.data), ctypes.byref(yw_in_dim_1), ctypes.byref(yw_in_dim_2), ctypes.c_void_p(yw_in.ctypes.data), ctypes.byref(yw_dim_1), ctypes.byref(yw_dim_2), ctypes.c_void_p(yw.ctypes.data), ctypes.byref(agg_iterators_dim_1), ctypes.byref(agg_iterators_dim_2), ctypes.c_void_p(agg_iterators.ctypes.data), ctypes.byref(steps), ctypes.byref(record_present), ctypes.byref(record_dim_1), ctypes.byref(record_dim_2), ctypes.c_void_p(record.ctypes.data), ctypes.byref(sum_squared_error), ctypes.byref(continuing_present), ctypes.byref(continuing), ctypes.byref(info))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return config, model, rwork, iwork, lwork, ax_in, x_in, y_in, yw_in, yw, agg_iterators, (record if record_present else None), sum_squared_error.value, info.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine PROFILE
    
    def profile(self, subroutine_name):
        '''! Wrapper for retrieving a profile entry by name.'''
        MODEL_CONFIG = axy.MODEL_CONFIG
        
        # Setting up "subroutine_name"
        if ((not issubclass(type(subroutine_name), numpy.ndarray)) or
            (not numpy.asarray(subroutine_name).flags.f_contiguous) or
            (not (subroutine_name.dtype == numpy.dtype(ctypes.c_char)))):
            subroutine_name = numpy.asarray(subroutine_name, dtype=ctypes.c_char, order='F').reshape(-1)
        subroutine_name_dim_1 = ctypes.c_long(subroutine_name.shape[0])
        
        # Setting up "profile"
        profile = PROFILE_ENTRY()
    
        # Call C-accessible Fortran wrapper.
        clib.c_profile(ctypes.byref(subroutine_name_dim_1), ctypes.c_void_p(subroutine_name.ctypes.data), ctypes.byref(profile))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return profile

axy = axy()

