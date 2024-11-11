class ClassificationOption
    attr_accessor :id, :text, :sub_options
  
    def initialize(id:, text:, sub_options: nil)
      @id = id
      @text = text
      @sub_options = sub_options
    end
  end
  
daily_minor_planet_options = [
    ClassificationOption.new(id: 1, text: "Object cannot be followed"),
    ClassificationOption.new(id: 2, text: 'Object follows green circle consistently'),
    ClassificationOption.new(id: 3, text: "Varied/unknown")
];

  jvh_options = [
    ClassificationOption.new(id: 1, text: "Vortex"),
    ClassificationOption.new(id: 2, text: "Turbulent region"),
    ClassificationOption.new(id: 3, text: "Cloud bands"),
    ClassificationOption.new(id: 4, text: "None of the above/content too blurry")
  ]
  
  daily_minor_planet_options = [
    ClassificationOption.new(id: 1, text: "Object cannot be followed"),
    ClassificationOption.new(id: 2, text: "Object follows green circle consistently"),
    ClassificationOption.new(id: 3, text: "Varied/unknown")
  ]
  
  planet_four_options = [
    ClassificationOption.new(id: 1, text: "Dust Deposits"),
    ClassificationOption.new(id: 2, text: "Surface Cracks"),
    ClassificationOption.new(id: 3, text: "Spider-like Features"),
    ClassificationOption.new(id: 4, text: "Rocky Outcrops"),
    ClassificationOption.new(id: 5, text: "Smooth Terrain")
  ]
  
  automatonai_for_mars_options = [
    ClassificationOption.new(id: 1, text: "Big rocks"),
    ClassificationOption.new(id: 2, text: "Sand"),
    ClassificationOption.new(id: 3, text: "Soil"),
    ClassificationOption.new(id: 4, text: "Bedrock"),
    ClassificationOption.new(id: 5, text: "Unlabelled")
  ]
  
  cloud_classification_options_one = [
    ClassificationOption.new(id: 1, text: "White colour"),
    ClassificationOption.new(id: 2, text: "Blue colour")
  ]
  
  cloud_classification_options_two = [
    ClassificationOption.new(id: 1, text: "Bright clouds"),
    ClassificationOption.new(id: 2, text: "Faint clouds"),
    ClassificationOption.new(id: 3, text: "Medium clouds")
  ]
  
  cloud_classification_options_three = [
    ClassificationOption.new(id: 1, text: "Clouds cover most of the height"),
    ClassificationOption.new(id: 2, text: "Clouds are smaller")
  ]
  
  planet_classification_options = [
    ClassificationOption.new(id: 1, text: 'No dips at all'),
    ClassificationOption.new(id: 2, text: 'Repeating dips'),
    ClassificationOption.new(id: 3, text: 'Dips with similar size'),
    ClassificationOption.new(id: 4, text: 'Dips aligned to one side')
  ]
  
  rover_img_classification_options = [
    ClassificationOption.new(id: 1, text: 'Dried-up water channels'),
    ClassificationOption.new(id: 2, text: 'Pebbles/medium-sized rocks'),
    ClassificationOption.new(id: 3, text: 'Hills/mountain formations'),
    ClassificationOption.new(id: 4, text: 'Volcano (dormant/extinct)'),
    ClassificationOption.new(id: 5, text: 'Mineral deposits'),
    ClassificationOption.new(id: 6, text: 'Sandy/rocky terrain')
  ]
  
  lidar_earth_clouds_read_classification_options = [
    ClassificationOption.new(id: 1, text: "Nimbostratus"),
    ClassificationOption.new(id: 2, text: 'Cumulonimbus'),
    ClassificationOption.new(id: 3, text: 'Stratocumulus'),
    ClassificationOption.new(id: 4, text: 'Stratus'),
    ClassificationOption.new(id: 5, text: "Cumulus"),
    ClassificationOption.new(id: 6, text: "Altostratus"),
    ClassificationOption.new(id: 7, text: "Altocumulus"),
    ClassificationOption.new(id: 8, text: "Cirrostratus"),
    ClassificationOption.new(id: 9, text: "Cirrocumulus"),
    ClassificationOption.new(id: 10, text: "Cirrus"),
    ClassificationOption.new(id: 11, text: "No clouds")
  ]
  
  plankton_portal_classification_options = [
    ClassificationOption.new(id: 1, text: 'Round plankton, no tentacles'),
    ClassificationOption.new(id: 2, text: "Head with tail"),
    ClassificationOption.new(id: 3, text: 'Jellyfish-like'),
    ClassificationOption.new(id: 4, text: 'Bug-like'),
    ClassificationOption.new(id: 5, text: "Ribbon/elongated"),
    ClassificationOption.new(id: 6, text: "Unidentifiable/None")
  ]
  
  disk_detector_classification_options = [
    ClassificationOption.new(id: 1, text: "Object moves away from crosshairs"),
    ClassificationOption.new(id: 2, text: "Object is extended beyond the outer circle"),
    ClassificationOption.new(id: 3, text: "Multiple objects inside inner circle"),
    ClassificationOption.new(id: 4, text: "Objects between inner and outer circles"),
    ClassificationOption.new(id: 5, text: "Object is not round"),
    ClassificationOption.new(id: 6, text: "None of the above")
  ]
  
  penguin_watch_classification_options = [
    ClassificationOption.new(id: 1, text: "Adult penguin"),
    ClassificationOption.new(id: 2, text: "Penguin chicks"),
    ClassificationOption.new(id: 3, text: "Penguin eggs"),
    ClassificationOption.new(id: 4, text: "Nesting pair with eggs"),
    ClassificationOption.new(id: 5, text: "No penguins/too blurry")
  ]
  
  initial_cloud_classification_options = [
    ClassificationOption.new(id: 1, text: "Narrow arch"),
    ClassificationOption.new(id: 2, text: "Wide arch"),
    ClassificationOption.new(id: 3, text: "1 cloud"),
    ClassificationOption.new(id: 4, text: "2 clouds"),
    ClassificationOption.new(id: 5, text: "3 clouds"),
    ClassificationOption.new(id: 6, text: "4+ clouds")
  ]
  
  zoodex_burrowing_owl_classification_options = [
    ClassificationOption.new(id: 1, text: "Adult owl"),
    ClassificationOption.new(id: 2, text: "Baby owl"),
    ClassificationOption.new(id: 3, text: 'Mortality event'),
    ClassificationOption.new(id: 4, text: "Infanticide"),
    ClassificationOption.new(id: 5, text: "Prey delivery"),
    ClassificationOption.new(id: 6, text: "Mating"),
    ClassificationOption.new(id: 7, text: "Feeding"),
    ClassificationOption.new(id: 8, text: "Owls have bands")
  ]
  
  zoodex_iguanas_from_above_classification_options = [
    ClassificationOption.new(id: 1, text: "Adult Male not in a Lek"),
    ClassificationOption.new(id: 2, text: "Adult male with a Lek"),
    ClassificationOption.new(id: 3, text: "Juvenile/Female"),
    ClassificationOption.new(id: 4, text: "Partial iguana")
  ]
  
  zoodex_south_coast_fauna_recovery = [
    ClassificationOption.new(id: 1, text: "Australian raven"),
    ClassificationOption.new(id: 2, text: "Red-winged fairy-wren"),
    ClassificationOption.new(id: 3, text: "Cat"),
    ClassificationOption.new(id: 4, text: "Brown falcon"),
    ClassificationOption.new(id: 5, text: "Silvereye"),
    ClassificationOption.new(id: 6, text: "Echidna"),
    ClassificationOption.new(id: 7, text: "Brown quail"),
    ClassificationOption.new(id: 8, text: "Southern emu-wren"),
    ClassificationOption.new(id: 9, text: "Fox"),
    ClassificationOption.new(id: 10, text: "Brush bronzewing"),
    ClassificationOption.new(id: 11, text: "Splendid fairy-wren"),
    ClassificationOption.new(id: 12, text: "Mouse or smaller?"),
    ClassificationOption.new(id: 13, text: "Carnaby's black cockatoo"),
    ClassificationOption.new(id: 14, text: "Spotted nightjar"),
    ClassificationOption.new(id: 15, text: "Quenda"),
    ClassificationOption.new(id: 16, text: "Common bronzewing"),
    ClassificationOption.new(id: 17, text: "Tawny frogmouth"),
    ClassificationOption.new(id: 18, text: "Quokka"),
    ClassificationOption.new(id: 19, text: "Emu"),
    ClassificationOption.new(id: 20, text: "Tawny-crowned honeyeater"),
    ClassificationOption.new(id: 21, text: "Rabbit"),
    ClassificationOption.new(id: 22, text: "Galah"),
    ClassificationOption.new(id: 23, text: "Wedge-tailed eagle"),
    ClassificationOption.new(id: 24, text: "Western brush wallaby"),
    ClassificationOption.new(id: 25, text: "Grey butcherbird"),
    ClassificationOption.new(id: 26, text: "Welcome swallow"),
    ClassificationOption.new(id: 27, text: "Western grey kangaroo"),
    ClassificationOption.new(id: 28, text: "Grey currawong"),
    ClassificationOption.new(id: 29, text: "Western bristlebird"),
    ClassificationOption.new(id: 30, text: "Australian magpie")
  ]  