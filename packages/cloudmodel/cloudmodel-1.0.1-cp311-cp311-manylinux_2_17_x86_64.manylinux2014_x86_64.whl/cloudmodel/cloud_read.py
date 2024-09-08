"""Module to read and compare cloud model data."""

import os
import re
from enum import Enum

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

from cloudmodel.constants import (
    Av0,
    Cp,
    Cv,
    G,
    Kapa,
    Lsl0,
    Lvl0,
    P00,
    Rd,
    Rv,
    T0,
    Vis0,
    Vtnie0,
    rhogra,
)
from cloudmodel.constants import (
    biased_nx1,
    inis_biased_nz1,
    inis_var_list,
    nube31_biased_nz1,
    nube31_var_list,
)
from cloudmodel.constants import dx1, nz1, nx1
from cloudmodel.interface import c_interface as nb
from cloudmodel.z_profile import (
    aerosol,
    air_density,
    air_density_recalc,
    crystal_efficiencies,
    hail_terminal_velocity,
    latent_heat,
    pp,
    pp2,
    rain_terminal_velocity,
    saturated_vapor_pressure2,
    snow_terminal_velocity,
    temperature,
    vapor,
    velocities,
    viscosity,
)

from scipy.io import FortranFile


class ImageStyle(Enum):
    """Enum to select the style of the image."""

    IMAGE = "Image"
    CONTOUR = "Contour"


class InputFileType(Enum):
    """Enum to select the input file."""

    NUBE31 = "Nube"
    INIS = "Inis"


class FolderHandle(Enum):
    """Enum to select how to respond if destiny folder exists."""

    IGNORE = "Ignore"
    DELETE = "Delete"
    CANCEL = "Cancel"


class CloudSimulation:
    """
    Represents a cloud model.

    Args
    ----
        simulation_time_minutes (int): The total simulation time in minutes.
        save_time_minutes (int): The time interval in minutes at which the
            model state is saved.
        statistic_time_minutes (int): The time interval in minutes at which
            statistics are calculated.
        backup_time_minutes (int): The time interval in minutes at which
            backups are created.
    """

    def __init__(
        self,
        simulation_time_minutes=0,
        save_time_minutes=0,
        statistic_time_minutes=0,
        backup_time_minutes=0,
        restore_backup=False,
        directory=".temp/",
        dx1=dx1,
        nz1=nz1,
        g=G,
        rd=Rd,
        rv=Rv,
        kapa=Kapa,
        t0=T0,
        p00=P00,
        lvl0=Lvl0,
        lsl0=Lsl0,
        vis0=Vis0,
        rhogra=rhogra,
        av0=Av0,
        vtnie0=Vtnie0,
        cp=Cp,
        cv=Cv,
        tlvl=None,
        tlsl=None,
        tlvs=None,
        telvs=None,
        tesvs=None,
        tvis=None,
        u_z_initial=None,
        v_z_initial=None,
        presi0=None,
        theta_z_initial=None,
        pres00=None,
        cc2=None,
        temperature_z_initial=None,
        air_density_z_initial=None,
        aerosol_z_initial=None,
        vapor_z_initial=None,
        av=None,
        vtnie=None,
        vtgra0=None,
    ):
        self.simulation_time_minutes = simulation_time_minutes
        self.save_time_minutes = save_time_minutes
        self.statistic_time_minutes = statistic_time_minutes
        self.backup_time_minutes = backup_time_minutes
        self.restore_backup = restore_backup
        if directory[-1] != "/":
            directory += "/"
        print(f"Destination directory: {directory}")
        self.directory = directory

        self.dx1 = dx1
        self.nz1 = nz1
        self.G = g
        self.Rd = rd
        self.Rv = rv
        self.Kapa = kapa
        self.T0 = t0
        self.P00 = p00
        self.Lvl0 = lvl0
        self.Lsl0 = lsl0
        self.Vis0 = vis0
        self.rhogra = rhogra
        self.Av0 = av0
        self.Vtnie0 = vtnie0
        self.Cp = cp
        self.Cv = cv
        if tlvl is None or tlsl is None or tlvs is None:
            l_heat = latent_heat()
            if tlvl is None:
                self.Tlvl = l_heat[0]
            if tlsl is None:
                self.Tlsl = l_heat[1]
            if tlvs is None:
                self.Tlvs = l_heat[2]
        if telvs is None or tesvs is None:
            s_vapor = saturated_vapor_pressure2(self.Tlvl, self.Tlvs)
            if telvs is None:
                self.Telvs = s_vapor[0]
            if tesvs is None:
                self.Tesvs = s_vapor[1]
        if tvis is None:
            self.Tvis = viscosity()
        if telvs is None or tesvs is None:
            cry_effic = crystal_efficiencies()
            if telvs is None:
                self.Eautcn = cry_effic[0]
            if tesvs is None:
                self.Eacrcn = cry_effic[1]
        if u_z_initial is None or v_z_initial is None:
            z_profile = velocities()
            if u_z_initial is None:
                self.u_z_initial = z_profile[0]
            if v_z_initial is None:
                self.v_z_initial = z_profile[1]
        if temperature_z_initial is None:
            self.temperature_z_initial = temperature()
        if aerosol_z_initial is None:
            self.aerosol_z_initial = aerosol()
        if vapor_z_initial is None:
            self.vapor_z_initial = vapor(
                self.temperature_z_initial, self.Telvs
            )
        if (av is None) or (vtnie is None):
            presi0_aux = pp()
            if av is None:
                self.Av = rain_terminal_velocity(presi0_aux)
            if vtnie is None:
                self.Vtnie = snow_terminal_velocity(presi0_aux)

        if vtgra0 is None:
            self.Vtgra0_in = hail_terminal_velocity(
                self.Tvis,
                self.temperature_z_initial,
                air_density(presi0_aux, self.temperature_z_initial),
            )
        if air_density_z_initial is None:
            self.air_density_z_initial = air_density_recalc(
                air_density(pp(), self.temperature_z_initial),
                self.vapor_z_initial,
            )
        if (
            (presi0 is None)
            or (theta_z_initial is None)
            or (pres00 is None)
            or (cc2 is None)
        ):
            presi0_aux = pp()
            pp2_aux = pp2(
                self.air_density_z_initial,
                presi0_aux,
                self.temperature_z_initial,
            )
            if presi0 is None:
                self.Presi0 = pp2_aux[0]
            if theta_z_initial is None:
                self.theta_z_initial = pp2_aux[1]
            if pres00 is None:
                self.Pres00 = pp2_aux[2]
            if cc2 is None:
                self.cc2 = pp2_aux[3]

        self.initial_analytics: FileStyle = None
        self.cloud_analytics: FileStyle = None

    def load_model(self):
        """Load the cloud model."""
        self.run_cloud_analysis()

    def get_cuts(self):
        """Get the cuts from the cloud model."""
        nb.get_cut_python()

    def run_model(self):
        """Run the cloud model."""
        check_path(FolderHandle.IGNORE.value, self.directory)
        nb.set_dimensions_python(self.dx1, self.nz1)
        nb.set_constants_python(
            self.G,
            self.Rd,
            self.Rv,
            self.Kapa,
            self.T0,
            self.P00,
            self.Lvl0,
            self.Lsl0,
            self.Vis0,
            self.rhogra,
            self.Av0,
            self.Vtnie0,
            self.Cp,
            self.Cv,
            self.Tlvl,
            self.Tlsl,
            self.Tlvs,
            self.Telvs,
            self.Tesvs,
            self.Tvis,
            self.Eautcn,
            self.Eacrcn,
        )
        nb.set_initial_z_state_python(
            self.temperature_z_initial,
            self.u_z_initial,
            self.v_z_initial,
            self.Presi0,
            self.air_density_z_initial,
            self.aerosol_z_initial,
            self.vapor_z_initial,
            self.theta_z_initial,
            self.Pres00,
            self.cc2,
        )

        nb.set_microphysics_perturbation_python(
            self.Av,
            self.Vtnie,
            self.Vtgra0_in,
        )

        check_path(FolderHandle.DELETE.value, self.directory, "cortes")

        nb.run_model_python(
            self.simulation_time_minutes,
            self.save_time_minutes,
            self.statistic_time_minutes,
            self.backup_time_minutes,
            self.restore_backup,
            self.directory,
        )
        self.load_model()

    def run_initial_analysis(self):
        """
        Run the initial analysis on the data.

        Returns
        -------
            FileStyle: An instance of the FileStyle class representing
                the analysis results.
        """
        data = FileStyle(
            chosen_file="Inis",
            output_data_path=self.directory,
            img_path="img/" + self.directory,
            img_option="Contour",
            folder_handle="Delete",
        )
        self.initial_analytics = data

    def run_cloud_analysis(self):
        """
        Run the cloud analysis.

        Returns
        -------
            FileStyle: The cloud analysis object.
        """
        data = FileStyle(
            chosen_file="Nube",
            output_data_path=self.directory,
            img_path="image/",
            img_option=ImageStyle.CONTOUR.value,
            folder_handle="Delete",
        )
        self.cloud_analytics = data

    def clean_model(self):
        """
        Clean the model by deleting the files in the specified directory.

        If the directory is set to ".temp/", this method will delete all
        the files in that directory using the `check_path` function with
        the `FolderHandle.DELETE` option.

        Note: This method assumes that the `check_path` function is defined
            elsewhere.

        Returns
        -------
            None
        """
        if self.directory == ".temp/":
            check_path(FolderHandle.DELETE.value, self.directory)

    def generate_cut_image(self, filename="cut_image.png"):
        cut_dir = f"{self.directory}cortes/"
        part = ["GO", "LL", "CR", "NI", "GR"]
        colores = ["r", "tab:orange", "c", "b", "g"]
        pos = "y"

        vec = np.ones([nz1, nx1, len(part), 1])

        for i, nom in enumerate(part):
            nombre = nom + pos + "17"
            vec[:, :, i, 0] = np.genfromtxt(f"{cut_dir}{nombre}")
        plt.figure(figsize=[10, 10])
        plt.ylim(0, 35)
        plt.xlim(10, 40)
        plt.xlabel("X", fontsize=20)
        plt.ylabel("Z", fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        for i in range(len(part)):
            plt.contour(vec[:, :, i, 0], [10, 500], colors=colores[i])

        plt.savefig(f"{cut_dir}{filename}")


class FileStyle:
    """
    A class representing the file style for cloud data.

    Attributes
    ----------
        chosen_file (str): The chosen input file type.
        output_data_path (str): The path to the output data folder.
        img_path (str): The path to the image folder.
        img_option (str): The image style option.
        folder_handle (str): The folder handling option.

    Methods
    -------
        _get_data(): Get the data from the selected files.
        _get_var_from_data(file_number, var_iterator): Get a variable
            from the data.
        get_var(var, time): Get a specific variable at a given time.
        show_var_dataframe(var_array, center, axis): Show a variable as
            a DataFrame.
        center_var(var_array, center, axis): Center a variable along a
            given axis.
        get_var_max_value_position(var_array): Get the position of the
            maximum value in a variable.
        _plot_style(variable): Plot the style of a variable.
        parse_status_img(): Animates the variables in the given var_list.
    """

    def __init__(
        self,
        chosen_file=InputFileType.NUBE31.value,
        output_data_path=".temp/",
        img_path="img/",
        img_option=ImageStyle.IMAGE.value,
        folder_handle=FolderHandle.IGNORE.value,
    ):
        if output_data_path[-1] != "/":
            output_data_path += "/"
        self.output_data_path = output_data_path
        self.img_path = f"{output_data_path}{img_path}"
        self.data_file = []
        self.folder_handle = folder_handle
        match chosen_file:
            case InputFileType.NUBE31.value:
                self.img_option = img_option
                self.var_list = nube31_var_list  # list of variables to plot
                self.var_amount = len(
                    nube31_var_list
                )  # amount of variables to plot per file
                self.binary_regex = r".sal$"  # regex to match binary files
                self.data_dimension = 3  # dimension of the data
                self.var_datatype = np.float32  # datatype of the variables
                self.var_structure_size = (
                    biased_nx1 * biased_nx1 * nube31_biased_nz1
                )  # size of the variables
                self.var_structure = (
                    biased_nx1,
                    biased_nx1,
                    nube31_biased_nz1,
                )  # structure of the variables
                self.file_name = "sal"
            case InputFileType.INIS.value:
                self.img_option = ImageStyle.IMAGE.value
                self.var_list = inis_var_list
                self.var_amount = len(inis_var_list)
                self.binary_regex = r"inis.da$"
                self.data_dimension = 1
                self.var_datatype = np.float32  # datatype of the variables
                self.var_structure_size = inis_biased_nz1  # var size
                self.var_structure = inis_biased_nz1  # var structure
                self.file_name = "inis"
            case _:
                raise ValueError("Invalid Input File Type")
        self._get_data()

    def _get_data(self):
        """Get the data from the selected files."""
        selected_files = _get_file_list(
            self.output_data_path, self.binary_regex
        )
        for file in selected_files:
            with FortranFile(f"{self.output_data_path}{file}", "r") as f:
                self.data_file.append(f.read_reals(self.var_datatype))

    def _get_var_from_data(self, file_number, var_iterator) -> np.ndarray:
        """
        Get a variable from the data.

        Args
        ----
            file_number (int): The index of the file in the data_file list.
            var_iterator (int): The iterator for the variable in the file.

        Returns
        -------
            numpy.ndarray: The variable data as a numpy array.
        """
        actual_file_data = self.data_file[file_number]
        return actual_file_data[
            var_iterator : var_iterator + self.var_structure_size
        ].reshape(self.var_structure, order="F")

    def get_var(self, var: str, time: int):
        """
        Get a specific variable at a given time.

        Args
        ----
            var (str): The name of the variable.
            time (int): The time index. (nube01.sal <= time <= nube**.sal)

        Raise:
        ------
            ValueError: If the variable is not in the variable list.

        Returns
        -------
            numpy.ndarray: The variable data as a numpy array.
        """
        var_index = self.var_list.index(var)
        var_iterator = var_index * self.var_structure_size
        return self._get_var_from_data(time, var_iterator)

    def get_var_dataframe(self, var_array, center: tuple, axis: str):
        """
        Show a variable as a DataFrame.

        Args
        ----
            var_array (numpy.ndarray): The variable data as a numpy array.
            center (tuple): The center coordinates for the variable.
            axis (str): The axis along which to center the variable.
        """
        return pd.DataFrame(self.center_var(var_array, center, axis))

    def center_var(self, var_array, center: tuple, axis: str):
        """
        Center a variable along a given axis.

        Args
        ----
            var_array (numpy.ndarray): The variable data as a numpy array.
            center (tuple): The center coordinates for the variable.
                can be provided by _get_var_max_value_position.
            axis (str): The axis along which to center the variable.
                options: "x", "y", "z"

        Returns
        -------
            numpy.ndarray: The centered variable data as a numpy array.
        """
        match axis:
            case "x":
                return var_array[center[0][0], :, :]
            case "y":
                return var_array[:, center[1][0], :]
            case "z":
                return var_array[:, :, center[2][0]]
            case _:
                raise ValueError("Invalid Axes")

    def _get_var_max_value_position(self, var_array):
        """
        Get the position of the maximum value in a variable.

        Args
        ----
            var_array (numpy.ndarray): The variable data as a numpy array.

        Returns
        -------
            tuple: The position of the maximum value in the variable.
        """
        return np.where(var_array == np.max(var_array))

    def _plot_style(self, variable):
        """
        Apply a specific plot style based on the image option and data dimen.

        Parameters
        ----------
            variable (numpy.ndarray): The variable to be plotted.

        Raises
        ------
            ValueError: If the image style is invalid.

        Returns
        -------
            None
        """
        match self.img_option:
            case ImageStyle.IMAGE.value:
                if self.data_dimension == 3:
                    plt.imshow(
                        self.center_var(
                            variable,
                            self._get_var_max_value_position(variable),
                            "z",
                        )
                        # np.flipud(variable[:, :, plot_center])
                    )
                elif self.data_dimension == 1:
                    plt.plot(variable[3:-3])  # Cleans trash data
            case ImageStyle.CONTOUR.value:
                fig, ax = plt.subplots()
                cs = ax.contour(
                    # np.flipud(variable[:, :, plot_center]),
                    self.center_var(
                        variable,
                        self._get_var_max_value_position(variable),
                        "z",
                    ),
                    linewidths=0.3,
                    colors="k",
                )
                ax.clabel(cs, fontsize=6, inline=True)
            case _:
                raise ValueError("Invalid Image Style")
        plt.grid(False)
        plt.style.use("fivethirtyeight")
        # plt.colorbar() # Generates infinite colorbars in animation
        plt.xlabel("X")
        plt.ylabel("Y")

    def parse_status_img(self, img_option):
        """
        Parse the status image data and generates plots for each variable.

        This method iterates over the data files and generates plots for
        each variable in the status image. The plots are saved as PNG
        images in the specified image path.

        Returns
        -------
            None
        """
        self.img_option = img_option
        check_path(self.folder_handle, f"{self.img_path}{self.file_name}")
        for file_iterator in range(len(self.data_file)):
            full_img_path = (
                f"{self.img_path}{self.file_name}/{str(file_iterator)}/"
            )
            check_path(self.folder_handle, full_img_path)
            var_iterator = 0
            for structure_iterator in range(
                0, len(self.data_file[file_iterator]), self.var_structure_size
            ):
                variable = self._get_var_from_data(
                    file_iterator, structure_iterator
                )
                filenumber = str(file_iterator)
                plt.title(f"{filenumber} {self.var_list[var_iterator]}")
                self._plot_style(variable)
                dirname = f"{self.img_path}{self.file_name}"
                filename = f"{self.var_list[var_iterator]}.png"
                plt.savefig(f"{dirname}/{filenumber}/{filename}")
                plt.close()  # If not closed, images will be superimposed
                if var_iterator < self.var_amount:
                    var_iterator += 1
                else:
                    var_iterator = 0

    def multi_var_img(self, var_1, var_2):
        """
        Plot two INITIAL variables against each other.

        Args
        ----
            var_1 (int): Index of the first variable to plot.
            var_2 (int): Index of the second variable to plot.

        Returns
        -------
            None
        """
        check_path(
            self.folder_handle, f"{self.img_path}{self.file_name}/multivar/"
        )
        var_index = self.var_list.index(var_1)
        var_index_2 = self.var_list.index(var_2)
        var_iterator = var_index * self.var_structure_size
        var_iterator_2 = var_index_2 * self.var_structure_size
        var_1_data = self._get_var_from_data(0, var_iterator)
        var_2_data = self._get_var_from_data(0, var_iterator_2)
        var_1_name = self.var_list[var_index]
        var_2_name = self.var_list[var_index_2]
        plt.title(f"{var_1_name} vs {var_2_name}")
        try:
            plt.plot(var_1_data[10:-10], var_2_data[10:-10], ".b")
        except ValueError as e:
            raise ValueError("Only Inis type file") from e
        dirname = f"{self.img_path}{self.file_name}"
        filename = f"{var_1_name}_{var_2_name}.png"
        plt.savefig(f"{dirname}/multivar/{filename}")
        plt.close()  # If not closed, images will be superimposed


def _get_file_list(data_path, binary_regex):
    """
    Get a sorted list of files in the specified data path that match the given.

        binary regex pattern.

    Args
    ----
        data_path (str): The path to the data directory.
        binary_regex (str): The regular expression pattern to match binary
            files.

    Returns
    -------
        list: A sorted list of file names that match the binary regex pattern.
    """
    files = os.listdir(data_path)  # List all files in outputdata folder
    reg = re.compile(binary_regex)  # Compile regex to match binary files
    return sorted(filter(reg.search, files))


def check_path(folder_handle, path, selected_file_name=""):
    """
    Check if a path exists and create it if necessary.

    Args
    ----
        folder_handle (str): The handling option for existing folders.
        path (str): The path to check and create if necessary.
        selected_file_name (str): The name of the selected file (default is
            empty string).

    Raises
    ------
        ValueError (str): If the folder handle is invalid or the folder already
            exists (depending on the handling option).
    """
    if path[-1] != "/":
        path += "/"
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.exists(path + selected_file_name + "/"):
        os.makedirs(path + selected_file_name + "/")
    else:
        match folder_handle:
            case FolderHandle.IGNORE.value:
                return
            case FolderHandle.DELETE.value:
                os.system(f"rm -rf {path}{selected_file_name}/*")
            case FolderHandle.CANCEL.value:
                raise ValueError("Folder already exists")
            case _:
                raise ValueError("Invalid Folder Handle")
