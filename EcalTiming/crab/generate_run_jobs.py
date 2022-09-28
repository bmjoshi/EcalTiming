import os
from random import random
from datetime import datetime

template_file = 'CRAB_run_job_template.py'
with open(template_file, 'r') as f0:
    tmp_lines = f0.readlines()

globaltag = '124X_dataRun3_Prompt_v4'

tstamp = datetime.now()
date = '{}{}{}{}{}{}'.format(tstamp.day,tstamp.month,tstamp.year,tstamp.hour,tstamp.minute,tstamp.second)

runmap = {
    "357885": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/885/00000/49eefba4-c6e4-4f43-9ae1-85ca31c5eb94.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/885/00000/df3b688f-5d14-498c-bdc6-7d03b9e755f4.root"
    ],
    "357886": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/886/00000/46bc6a90-172f-491d-bc1b-a53ad5e8769d.root"
    ],
    "357887": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/887/00000/b11a476c-70d9-49d6-abe7-74f33e3cc201.root"
    ],
    "357888": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/888/00000/1d224b32-2212-4678-9cd5-ee03b8781fa5.root"
    ],
    "357889": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/889/00000/a3058901-1fc9-4a35-9cf3-c9e5e4513906.root"
    ],
    "357890": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/890/00000/7cbbdf8b-cfe1-46ba-9b5b-50095f4572f8.root"
    ],
    "357891": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/891/00000/6e32627a-f109-4df5-92d2-ecc37f1ffe68.root"
    ],
    "357892": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/892/00000/0d3728ad-701f-415a-ab92-9e087ef0cdf8.root"
    ],
    "357893": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/893/00000/d06f2b16-9de9-48c4-ac27-255b31eb4d69.root"
    ],
    "357894": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/894/00000/8b619623-58e2-41a0-b229-3310b41eea94.root"
    ],
    "357895": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/895/00000/6327ed02-27bd-4f52-857b-e9235553596c.root"
    ],
    "357896": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/896/00000/30d31317-4cc1-44fe-a035-48e0f1142027.root"
    ],
    "357897": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/897/00000/700cac56-6a58-475a-bca1-3fdf9b05f162.root"
    ],
    "357898": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/898/00000/ab726fc8-553c-422a-aee5-07904f104995.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/898/00000/ba4cc4b9-cf62-4f1d-87f4-baf1ca19e5f6.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/898/00000/9d1c55b0-1c3b-48de-9185-a3ddef743a65.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/898/00000/2ed3d481-64c1-4443-836b-04e3e97c44c3.root"
    ],
    "357899": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/dce9ca6b-79d3-4256-8f68-57ab96644ee7.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/e7e47f36-23f8-48e2-a48d-7b9217d49201.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/ec5c2d78-3a7d-4878-9b15-b10bc47f94fe.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/13255a45-3dde-4c58-bf29-162a275b7edf.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/716f1401-a118-4eeb-a7a9-bcbeb059d863.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/02e3bdbf-4f8e-493b-85e8-6b464f04d306.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/7196b871-3936-479b-8798-f467e22d6ae1.root"
    ],
    "357900": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/900/00000/3f976b3c-c7bd-4e00-ab25-de036381efe9.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/900/00000/3671b521-acc3-4979-b26f-2acdd29b3f8b.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/900/00000/0c22207c-62b0-4921-95d9-879927582ac8.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/900/00000/52bd964e-4d74-490a-be5a-d95cf2b43058.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/900/00000/2cb06620-9471-4cc6-8e6d-92728cd6313a.root"
    ],
    "357901": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/901/00000/eac27fd6-34a0-4c85-8037-4654b895d78a.root"
    ],
    "357902": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/902/00000/c429daca-9ed6-4ff1-ac71-e33121ae03c3.root"
    ],
    "357899": [
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/dce9ca6b-79d3-4256-8f68-57ab96644ee7.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/e7e47f36-23f8-48e2-a48d-7b9217d49201.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/ec5c2d78-3a7d-4878-9b15-b10bc47f94fe.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/13255a45-3dde-4c58-bf29-162a275b7edf.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/716f1401-a118-4eeb-a7a9-bcbeb059d863.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/02e3bdbf-4f8e-493b-85e8-6b464f04d306.root",
        "/store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/899/00000/7196b871-3936-479b-8798-f467e22d6ae1.root"
    ] 
        }
'''
runmap = {
           "356997": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/997/00000/4d8de230-7737-43e0-bdb4-ee2a1703e787.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/997/00000/a590edf4-4565-4d8a-b2da-4b57e5268413.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/997/00000/c5a78646-4425-40af-a30e-8cb694b8fd86.root"
    ],
    "356998": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/998/00000/5d9ab9bb-2351-4a10-9602-b7d2fb011ddc.root"
    ],
    "356999": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/999/00000/99be1020-43fe-4b55-a53f-1461b39e6f72.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/999/00000/abe0dac2-7d4c-453e-aee6-ea2648e274ff.root"
    ],
    "357000": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/000/00000/6637a592-e09b-4b1d-b08f-452a6dcc5616.root"
    ],
    "357001": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/001/00000/3a1fb6d2-99a9-4e92-8578-819ecc062e68.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/001/00000/084e1c17-83ab-4f13-8afc-027b40bdc91f.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/001/00000/9613bd0d-42c1-4053-9998-4731684c11ad.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/001/00000/fa4a5cc1-481f-4267-83e1-eed3e0d5a7ab.root"
    ],
    "357401": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/3137eeeb-6cf7-456d-93c8-9e7c04d72ccc.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/277e370c-e6cb-4ffe-b699-282bb7060d84.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/0218542e-ac3c-4041-9173-f00c40d616f0.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/f6b592bc-a932-4c6c-b41e-1ca14a905e3d.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/a254621d-6c97-482e-b380-57721b99c7a0.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/bbd598b6-e272-4630-859b-c8f604b5d7cc.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/610ffe4b-83ae-4095-b6a4-820c9f03a1a7.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/b0af5f10-c73c-400d-ae3f-1eba66867efb.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/7ebab728-8217-469e-be8a-98ac5f561ab1.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/52b62e35-f8ff-4a1f-974d-bcfde90c00d4.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/84dd40a0-2168-4a0d-86d6-42985a60b03d.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022C/AlCaPhiSym/RAW/v1/000/357/401/00000/625af40d-f4e7-4dfb-a718-bae068ecec9e.root"
    ]  
        }

runmap = {
    "357776": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/776/00000/714f123d-4d21-4a88-8148-16854d0a5c87.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/776/00000/328c9ca1-74a1-4448-8339-ff9dae59c64c.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/776/00000/bae72521-a490-49ea-8717-36ff85d9496b.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/776/00000/c09bf0ce-27f4-4dbe-a014-0c1677002530.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/776/00000/3b2080bb-5f0e-44c2-b356-bfa448ff1aab.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/776/00000/19d0b7f3-1086-4540-97fb-45335613ea2e.root"
    ],
    "357777": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/777/00000/5aaacb65-8fb9-43cc-853e-6ad2c51467c6.root"
    ],
    "357778": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/778/00000/6c92b8aa-da07-41f6-9712-9edefdb455e8.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/778/00000/899dd78b-f978-437c-b348-58cb6a49004e.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/778/00000/14521488-b7db-431e-bf44-b02132138798.root",
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/778/00000/3a69161f-d0ee-4eb9-91fc-4bbde53dfe81.root"
    ],
    "357779": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/779/00000/d7c4b27f-e324-4b1a-b0e3-581e99a711fe.root"
    ],
    "357780": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/780/00000/2f1bca59-8292-46bf-97f8-6974fbbea2ea.root"
    ],
    "357781": [
        "root://cms-xrd-global.cern.ch//store/data/Run2022D/AlCaPhiSym/RAW/v1/000/357/781/00000/7220af28-2e26-4e44-bb6f-9a7df7888122.root"
    ]}

runmap =    {
    "356371": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/371/00000/ddd301f7-dd28-401f-a636-1fcece41dcbe.root"
    ],
    "356375": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/375/00000/c18d5283-cb6f-4b6e-9ddd-46d634d0c14a.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/375/00000/68e69cfb-582a-4da2-995a-aee1fb8cca04.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/375/00000/9bfbab32-afeb-4507-9b78-d7c178d2089b.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/375/00000/0e0cd8c5-1180-4077-a443-cea0e3aafcd8.root"
    ],
    "356377": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/377/00000/1be84932-0ed0-4a25-b2d5-3f0739764891.root"
    ],
    "356378": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/bd768992-66c1-49bb-871f-46b6dbcbcc1c.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/afb82dda-0864-4314-8db9-47cbec24a2d6.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/a0f24bbe-fbf8-41d3-8644-dee9f9d29e12.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/db14f317-0d3c-4330-aa11-c361c59c17a8.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/3e4eb32b-36dc-48fd-8a81-638edf083e6d.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/b72b0c33-54b4-4549-8640-73306953fd50.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/8a88f19f-8cdc-4d14-9344-06c645b51b35.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/378/00000/087c7299-e6e2-4727-a8e2-1dc596674df6.root"
    ],
    "356381": [
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/af1990ce-1b07-4ef8-aa98-70ae52db9cbf.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/ff1c6893-5511-4e60-8253-da2d7413a139.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/2ce6b9db-e1fd-41d5-a4c6-02481128c4b6.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/f850b755-ca6f-483e-a6f4-6438efd5cc2f.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/d994f541-262f-45d6-9ca4-7fb87ad8cbcc.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/50112745-446c-44e8-ae41-abd3421d6ee5.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/736e5d27-da14-4c95-9bb7-adb0728fc9bb.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/6ba06bda-34af-44ed-a080-5e9adff490fe.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/f69bbff9-21c5-4092-888e-b86c70d25917.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/10c91f4c-84cf-42a4-8041-170b27e54970.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/c9a1175e-3b48-4048-bf39-63b826f2b9dc.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/e53fda37-be8c-4c48-b3fd-acb63441c33f.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/48e60cf8-1020-4fe5-a388-74d49ef0d4f9.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/99707340-7692-433f-8a2e-fac4927daab7.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/2292de79-5077-4bf2-a14d-14242751d210.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/af9d3ae2-1d9a-436c-a65e-e9cdf47bee66.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/262f55b1-4d4a-497a-b19c-7a95c19c4891.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/021ff086-2ec5-4941-8cbc-d5f8a8938e47.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/5b6a35a8-ee36-4d68-a39e-86595a9e4115.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/2478c8ea-c4df-4204-8d1b-a1e969845b0e.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/4891361e-b650-4bc7-8936-717ca849f5d1.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/f8826ecb-7ac0-4d78-815e-955515c69383.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/98f39fc0-cec4-4e57-ba1d-55235b6f8376.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/7facfad1-883b-4c04-98dc-bf23e0af4904.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/87b41aba-0021-4328-b45f-16a851dcd500.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/4407ecd4-6ae2-47a3-8d9c-f0f2ee90b6ce.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/f5f77b4e-4350-4ee8-a60e-90ec0c409fac.root",
        "/store/data/Run2022C/AlCaPhiSym/RAW/v1/000/356/381/00000/616bd279-6d50-4cec-904d-b65f98dbeb5d.root"
    ]
}
'''

for run in runmap:
   lines = [l for l in tmp_lines]
   files = '","'.join(runmap[run])
   files = '"'+files+'"'
   nfiles = len(runmap[run])
   with open('crab_Production_{}_{}.py'.format(date, run), 'w') as f0:
      for line in lines:
          if '<DATE>' in line: line = line.replace('<DATE>', date)
          if '<RUN>' in line: line = line.replace('<RUN>', run)
          if '<GT>' in line: line = line.replace('<GT>', globaltag)
          if '<NFILES>' in line: line = line.replace('<NFILES>', '1')
          if '<FILES>' in line: line = line.replace('<FILES>', files)
          f0.write(line)
   print('crab submit -c crab_Production_{}_{}.py'.format(date, run))
