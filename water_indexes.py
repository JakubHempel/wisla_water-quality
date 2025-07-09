import ee

indices_description = {
    "SABI": {
        "name": "🦠 SABI – Surface Algal Bloom Index",
        "description": "It was developed by (Alawadi 2010) to identify the presence of biomass in water, using the NIR band, which is sensitive to green plants, Blue band (responsive to pure water), and Green band, which detect algal blooms within the water column. "
        "Algae bloom phenomenon are most likely to happen when the suitable conditions of sunlight, high water temperature and high level of nutrients exists. "
        "Moreover, highly eutrophic waters can help algae feed due to their high nitrogen and phosphorus content (Caballero et al. 2020). "
        "The range of index values for water is from -0.1 to 0 and approximately -0.2 and lower for microalgae (Kulawiak 2016).",
        "formula": r'''SABI = \frac{NIR - Red}{Blue + Green} = \frac{B8 - B4}{B2 + B3}''',
        "ref": """<ul><li>F. Alawadi, 2010 <i>"Detection of surface algal blooms using the newly developed algorithm surface algal bloom index (SABI)"</i>, SPIE Proceedings: Remote Sensing of the Ocean, Sea Ice, and Large Water Regions 2010, t. 7825, n. 782506. doi:10.1117/12.862096.</li>
                      <li>I. Caballero, R. Fernández, O. M. Escalante, L. Maman, G. Navarro, 2020 <i>"New capabilities of Sentinel-2A/B satellites combined with in situ data for monitoring small harmful algal blooms in complex coastal waters."</i>, Sci Rep, t. 10, n. 8743. doi:10.1038/s41598-020-65600-1.</li>
                      <li>M. Kulawiak, 2016 <i>"Operational algae bloom detection in the Baltic Sea using GIS and AVHRR data."</i>, BALTICA, t. 29, n. 1, s. 3-18. doi:10.5200/baltica.2016.29.02.</li>
                  </ul>"""
    },
    "CGI": {
        "name": "🦠 CGI – Chlorophyll Green Index",
        "description": "In general, the chlorophyll index is applied to determine the total amount of chlorophyll in plants. "
                       "This variation uses the SWIR (resolution 60 meters and central wavelength at 945 nm) and Green channels in calculations.",
        "formula": r'''CGI = \frac{SWIR}{Green}-1''',
        "ref": """"""
    },
    "CDOM": {
        "name": "🦠 CDOM – Colored Dissolved Organic Matter",
        "description": "Is a water quality indicator used to assess optically active organic materials in water. "
                       "This parameter is influenced by two primary sources of organic matter. "
                       "The first source is the organic material that forms within the water body itself, such as phytoplankton. "
                       "The second source is organic matter that enters the water from external sources, like coal that may leach from the surrounding soil. "
                       "It has also been demonstrated that there is a correlation between content of methylmercury and CDOM in rivers (Fichot et al. 2016).",
        "formula": r'''CDOM = 537 \cdot \exp\left(-2.93 \cdot \frac{Green}{Red}\right)''',
        "ref": """<ul><li>Fichot C.G., Downing B.D., Bergamaschi B.A., Windham-Myers L., Marvin-DiPasquale M., Thompson D.R., Gierach M.M. 2016. <i>"High-Resolution Remote Sensing of Water Quality in the SanFrancisco Bay−Delta Estuary."</i>, Environmental Science and Technology, 50. doi:10.1021/acs.est.5b03518.</li></ul>"""
    },
    "DOC": {
        "name": "🦠 DOC – Dissolved Organic Carbon",
        "description": "Refers to the presence of organic carbon compounds that are dissolved in the water. "
                       "It serves as a key indicator of water quality, with higher levels often indicating pollution and potential for undesirable biological growth. "
                       "DOC may also be influenced by the density of other dissolved substances, such as metals. "
                       "Organic matter levels in the river are closely related to rainfall/runoff events, seasons and operational practices and typically range from 0.1 mg :small[$L^{-1}$] to 10-20 mg :small[$L^{-1}$] in fresh waters (Volk et al. 2002).",
        "formula": r'''DOC = 432 \cdot \exp\left(-2.24 \cdot \frac{Green}{Red}\right)''',
        "ref": """<ul><li>Volk C., Wood L., Johnson B., Robinson J., Wei Zhu H., Kaplan L. 2002. <i>"Monitoring dissolved organic carbon in surface and drinking waters."</i>, Journal of Environmental Monitoring, 4, 43-47. doi:10.1039/B107768F.</li></ul>"""
    },
    "Cyanobacteria": {
        "name": "🦠 Cyanobacteria",
        "description": "The values of this parameter are primarily linked to the presence of cyanobacterial blooms, which can be highly hazardous to humans, animals, and plants (Topp et al. 2020). "
        "Their blooms reduce the aesthetic value of recreational parts of water bodies. "
        "Moreover, cyanobacteria can produce both hepatotoxic peptides, such as Microcystis and Cyanopeptolin, which cause liver damage and are tumor-inducing (Hannson et al. 2007). "
        "The formula below was transformed for the Sentinel-2 satellite from algorithms created by Potes et al. (2011, 2012).",
        "formula": r'''Cyanobacteria = 115530.31 \cdot \left(\frac{Green \cdot Red}{Blue}\right)^{2.38} = \\
                                       115530.31 \cdot \left(\frac{B3 \cdot B4}{B2}\right)^{2.38}''',
        "ref": """<ul><li>M. S. Topp, N. Gokbuget, G. Zugmaier, A. S. Stein, H. Dombret, Y. Chen, J. Ribera, R. C. Bargou, H. Horst, H. M. Kantarjian, 2020. <i>"Long-term survival of patients with relapsed/refractory acute lymphoblastic leukemia treated with blinatumomab."</i>, American Cancer Society Journals, t. 127, n. 4, s. 554-559. doi:10.1002/cncr.33298.</li>
                      <li>L. A. Hannson, S. Gustafsson, K. Rengefors, L. Bomark, 2007. <i>"Cyanobacterial chemical warfare affects zooplankton community composition."</i>, Freshwater Biology, t. 52, n. 7, s. 1290-1301. doi:10.1111/j.1365-2427.2007.01765.x.</li>
                      <li>M. Potes, M. J. Costa, J. C. B. da Silva, A. M. Silva, M. Morais, 2011. <i>"Remote sensing of water quality parameters over Alqueva Reservoir in the south of Portugal."</i>, International Journal of Remote Sensing, t. 32 n. 12, s. 3373-3388. doi:10.1080/01431161003747513.</li>
                      <li>M. Potes, J. Costa, R. Salgado, 2012. <i>"Satellite remote sensing of water turbidity in Alqueva reservoir and implications on lake modelling."</i>, Hydrology and Earth System Sciences, t. 16, n. 6, s. 1623–1633. doi:10.5194/hess-16-1623-2012.</li>
                  </ul>"""
    },
    "Turbidity": {
        "name": "💦 Turbidity",
        "description": "Is a reduction in water clarity because of the presence of suspended matter absorbing or scattering light. "
        "Beyond its impact on the visual quality of rivers and recreational reservoirs, the transparency of the water affects changes in the amount of light available at different depths, influencing the process of photosynthesis (Izagirre et al. 2009). "
        "The formula below was transformed for the Sentinel-2 satellite from algorithms created by Potes et al. (2011, 2012).",
        "formula": r'''Turbidity = \frac{Red - Green}{Red + Green} = \frac{B4 - B3}{B4 + B3}''',
        "ref": """<ul><li>O. Izagirre, A. Serra, H. Guasch, A. Elosegi, 2009 <i>"Effects of sediment deposition on periphytic biomass, photosynthetic activity and algal community structure."</i>, Science of The Total Environment, t. 407, n. 21, s. 5694-5700. doi:10.1016/j.scitotenv.2009.06.049.</li>
                      <li>M. Potes, M. J. Costa, J. C. B. da Silva, A. M. Silva, M. Morais, 2011. <i>"Remote sensing of water quality parameters over Alqueva Reservoir in the south of Portugal."</i>, International Journal of Remote Sensing, t. 32 n. 12, s. 3373-3388. doi:10.1080/01431161003747513.</li>
                      <li>M. Potes, J. Costa, R. Salgado, 2012. <i>"Satellite remote sensing of water turbidity in Alqueva reservoir and implications on lake modelling."</i>, Hydrology and Earth System Sciences, t. 16, n. 6, s. 1623–1633. doi:10.5194/hess-16-1623-2012.</li> 
                  </ul>"""
    }
}


def water_indexes(image, only=None):
    available = {
        'NDWI': image.normalizedDifference(['B3', 'B8']).rename('NDWI'),
        'NDVI': image.normalizedDifference(['B8', 'B4']).rename('NDVI'),
        'NDSI': image.normalizedDifference(['B11', 'B12']).rename('NDSI'),
        'SABI': image.expression('(NIR - RED) / (BLUE + GREEN)',
                                 {'NIR': image.select('B8'), 'RED': image.select('B4'), 'BLUE': image.select('B2'), 'GREEN': image.select('B3')}).rename('SABI'),
        'CGI': image.expression('((SWIR / GREEN) - 1)',
                                {'SWIR': image.select('B9'), 'GREEN': image.select('B3')}).rename('CGI'),
        'CDOM': image.expression('537 * exp(-2.93 * GREEN / RED)',
                                 {'GREEN': image.select('B3'), 'RED': image.select('B4')}).rename('CDOM'),
        'DOC': image.expression('432 * exp(-2.24 * GREEN / RED)',
                                {'GREEN': image.select('B3'), 'RED': image.select('B4')}).rename('DOC'),
        'Cyanobacteria': image.expression('115530.31 * (GREEN * RED / BLUE) ** 2.38',
                                {'RED': image.select('B4'), 'BLUE': image.select('B2'), 'GREEN': image.select('B3')}).rename('Cyanobacteria'),
        'Turbidity': image.normalizedDifference(['B4', 'B3']).rename('Turbidity'),
        'AWEI': image.expression('4*(GREEN - SWIR1) - (0.25*NIR + 2.75*SWIR2)',
                                 {'GREEN': image.select('B3'), 'NIR': image.select('B8'), 'SWIR1': image.select('B11'), 'SWIR2': image.select('B12')}).rename('AWEI')
    }

    if only is not None:
        selected = [available[k] for k in only if k in available]
    else:
        selected = list(available.values())

    return image.addBands(ee.Image.cat(selected))
