# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_msr_goal.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetMSRGoal(object):
    def setupUi(self, PresetMSRGoal):
        if not PresetMSRGoal.objectName():
            PresetMSRGoal.setObjectName(u"PresetMSRGoal")
        PresetMSRGoal.resize(1196, 418)
        self.centralWidget = QWidget(PresetMSRGoal)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.goal_layout = QVBoxLayout(self.centralWidget)
        self.goal_layout.setSpacing(6)
        self.goal_layout.setContentsMargins(11, 11, 11, 11)
        self.goal_layout.setObjectName(u"goal_layout")
        self.goal_layout.setContentsMargins(6, 6, 6, 6)
        self.description_label = QLabel(self.centralWidget)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.goal_layout.addWidget(self.description_label)

        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setObjectName(u"label_2")

        self.goal_layout.addWidget(self.label_2)

        self.placed_slider_layout = QHBoxLayout()
        self.placed_slider_layout.setSpacing(6)
        self.placed_slider_layout.setObjectName(u"placed_slider_layout")
        self.placed_slider_layout.setContentsMargins(6, 6, 6, 6)
        self.placed_slider = QSlider(self.centralWidget)
        self.placed_slider.setObjectName(u"placed_slider")
        self.placed_slider.setMaximum(39)
        self.placed_slider.setPageStep(2)
        self.placed_slider.setOrientation(Qt.Horizontal)
        self.placed_slider.setTickPosition(QSlider.TicksBelow)

        self.placed_slider_layout.addWidget(self.placed_slider)

        self.placed_slider_label = QLabel(self.centralWidget)
        self.placed_slider_label.setObjectName(u"placed_slider_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.placed_slider_label.sizePolicy().hasHeightForWidth())
        self.placed_slider_label.setSizePolicy(sizePolicy)
        self.placed_slider_label.setMinimumSize(QSize(0, 0))
        self.placed_slider_label.setAlignment(Qt.AlignCenter)

        self.placed_slider_layout.addWidget(self.placed_slider_label)


        self.goal_layout.addLayout(self.placed_slider_layout)

        self.label = QLabel(self.centralWidget)
        self.label.setObjectName(u"label")

        self.goal_layout.addWidget(self.label)

        self.required_slider_layout = QHBoxLayout()
        self.required_slider_layout.setSpacing(6)
        self.required_slider_layout.setObjectName(u"required_slider_layout")
        self.required_slider_layout.setContentsMargins(6, 6, 6, 6)
        self.required_slider = QSlider(self.centralWidget)
        self.required_slider.setObjectName(u"required_slider")
        self.required_slider.setMaximum(39)
        self.required_slider.setPageStep(2)
        self.required_slider.setOrientation(Qt.Horizontal)
        self.required_slider.setTickPosition(QSlider.TicksBelow)

        self.required_slider_layout.addWidget(self.required_slider)

        self.required_slider_label = QLabel(self.centralWidget)
        self.required_slider_label.setObjectName(u"required_slider_label")

        self.required_slider_layout.addWidget(self.required_slider_label)


        self.goal_layout.addLayout(self.required_slider_layout)

        self.placement_group = QGroupBox(self.centralWidget)
        self.placement_group.setObjectName(u"placement_group")
        self.verticalLayout = QVBoxLayout(self.placement_group)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.restrict_placement_radiobutton = QRadioButton(self.placement_group)
        self.restrict_placement_radiobutton.setObjectName(u"restrict_placement_radiobutton")
        sizePolicy.setHeightForWidth(self.restrict_placement_radiobutton.sizePolicy().hasHeightForWidth())
        self.restrict_placement_radiobutton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.restrict_placement_radiobutton)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, -1, -1, -1)
        self.restrict_placement_label = QLabel(self.placement_group)
        self.restrict_placement_label.setObjectName(u"restrict_placement_label")
        self.restrict_placement_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.restrict_placement_label)

        self.prefer_metroids_check = QCheckBox(self.placement_group)
        self.prefer_metroids_check.setObjectName(u"prefer_metroids_check")
        sizePolicy.setHeightForWidth(self.prefer_metroids_check.sizePolicy().hasHeightForWidth())
        self.prefer_metroids_check.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.prefer_metroids_check)

        self.prefer_stronger_metroids_check = QCheckBox(self.placement_group)
        self.prefer_stronger_metroids_check.setObjectName(u"prefer_stronger_metroids_check")
        sizePolicy.setHeightForWidth(self.prefer_stronger_metroids_check.sizePolicy().hasHeightForWidth())
        self.prefer_stronger_metroids_check.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.prefer_stronger_metroids_check)

        self.prefer_bosses_check = QCheckBox(self.placement_group)
        self.prefer_bosses_check.setObjectName(u"prefer_bosses_check")
        sizePolicy.setHeightForWidth(self.prefer_bosses_check.sizePolicy().hasHeightForWidth())
        self.prefer_bosses_check.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.prefer_bosses_check)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.free_placement_radiobutton = QRadioButton(self.placement_group)
        self.free_placement_radiobutton.setObjectName(u"free_placement_radiobutton")
        sizePolicy.setHeightForWidth(self.free_placement_radiobutton.sizePolicy().hasHeightForWidth())
        self.free_placement_radiobutton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.free_placement_radiobutton)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, -1, -1, -1)
        self.free_placement_label = QLabel(self.placement_group)
        self.free_placement_label.setObjectName(u"free_placement_label")

        self.verticalLayout_3.addWidget(self.free_placement_label)


        self.verticalLayout.addLayout(self.verticalLayout_3)


        self.goal_layout.addWidget(self.placement_group)

        PresetMSRGoal.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetMSRGoal)

        QMetaObject.connectSlotsByName(PresetMSRGoal)
    # setupUi

    def retranslateUi(self, PresetMSRGoal):
        PresetMSRGoal.setWindowTitle(QCoreApplication.translate("PresetMSRGoal", u"Goal", None))
        self.description_label.setText(QCoreApplication.translate("PresetMSRGoal", u"<html><head/><body><p>In addition to just collecting the Baby, it is now necessary to collect Metroid DNA in order to reach Ridley. The minimum and maximum are limited to 0 and 39 DNA respectively. You can choose to have more DNA in the Pool than what is required to collect.</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("PresetMSRGoal", u"Controls how much Metroid DNA is obtainable.", None))
        self.placed_slider_label.setText(QCoreApplication.translate("PresetMSRGoal", u"0", None))
        self.label.setText(QCoreApplication.translate("PresetMSRGoal", u"Controls how much Metroid DNA is required to be collected.", None))
        self.required_slider_label.setText(QCoreApplication.translate("PresetMSRGoal", u"0", None))
        self.placement_group.setTitle(QCoreApplication.translate("PresetMSRGoal", u"Placement", None))
        self.restrict_placement_radiobutton.setText(QCoreApplication.translate("PresetMSRGoal", u"Restricted Placement", None))
        self.restrict_placement_label.setText(QCoreApplication.translate("PresetMSRGoal", u"<html><head/><body><p>The following options limit where Metroid DNA will be placed. There can only be as many DNA shuffled as there are preferred locations available. The first option adds 25 preferred locations, the second adds 14, and the third adds 4. In Multiworlds, DNA is guaranteed to be in your World.</p></body></html>", None))
        self.prefer_metroids_check.setText(QCoreApplication.translate("PresetMSRGoal", u"Prefer Standard Metroids (10 Alphas, 9 Gammas, 3 Zetas, 3 Omegas)", None))
        self.prefer_stronger_metroids_check.setText(QCoreApplication.translate("PresetMSRGoal", u"Prefer Stronger Metroids (7 Alpha+, 5 Gamma+, 1 Zeta+, 1 Omega+)", None))
        self.prefer_bosses_check.setText(QCoreApplication.translate("PresetMSRGoal", u"Prefer Bosses (Arachnus, Diggernaut Chase Reward, Diggernaut, Queen Metroid)", None))
        self.free_placement_radiobutton.setText(QCoreApplication.translate("PresetMSRGoal", u"Free Placement", None))
        self.free_placement_label.setText(QCoreApplication.translate("PresetMSRGoal", u"Enables DNA to be placed anywhere. For Multiworlds, this means even other Worlds.", None))
    # retranslateUi

