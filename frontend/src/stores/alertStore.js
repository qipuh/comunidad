import { reactive } from 'vue'

const alertState = reactive({
  visible: false,
  type: 'info',
  title: '',
  message: '',
  duration: 4000
})

export const alertStore = {
  state: alertState,

  show(title, message = '', type = 'info', duration = 4000) {
    alertState.visible = true
    alertState.type = type
    alertState.title = title
    alertState.message = message
    alertState.duration = duration
  },

  success(title, message = '', duration = 4000) {
    this.show(title, message, 'success', duration)
  },

  error(title, message = '', duration = 4000) {
    this.show(title, message, 'error', duration)
  },

  warning(title, message = '', duration = 4000) {
    this.show(title, message, 'warning', duration)
  },

  info(title, message = '', duration = 4000) {
    this.show(title, message, 'info', duration)
  },

  close() {
    alertState.visible = false
  }
}
